import requests
import enum
import datetime

DEBUG = True

API_HOST = "http://v5.vbb.transport.rest/"
API_GET_STATIONS = "stations"
API_GET_STOPS = "stops/"
API_GET_JOURNEY = "journeys"


class Modes(enum.Enum):
    """
    Enum of modes to indicate a operation type.
    """

    STATIONS_QUERY = 0
    STATIONS_ID = 1

    STOPS_ID = 2
    STOPS_ID_DEPARTURES = 3

    JOURNEY_BY_ID = 4


class Connections:
    """
    Holds information about multiple connections between origin and destination.
    """
    origin = None
    destination = None

    routes = None

    def __init__(self, origin, destination):
        self.origin = origin
        self.destination = destination

    def getConnections(self):
        response = makeJourneyRequest(self, Modes.JOURNEY_BY_ID)

        if response.status_code == 200:
            parseJourneyResponse(response.json(), self, Modes.JOURNEY_BY_ID)
        else:
            print("Got invalid response\nstatus={}\n".format(response.status_code))


class Journey:
    """
    Holds information about a single connection between origin and destination.
    """

    # TODO:
    # - add length of journey
    # - add start / stop date
    # - refreshing Details?
    # - delay

    origin = None
    destination = None

    legs = None
    numberTransfers = 0

    def __init__(self, origin, destination):
        self.origin = origin
        self.destination = destination

    def getTransfers(self):
        self.numberTransfers = len(self.legs) - 1

    def __str__(self):
        journeyString = "Transits: {}\nRoute:\n".format(self.numberTransfers)

        for l in self.legs:
            journeyString += str(l) + '\n'

        return journeyString


class Leg:
    """
    A leg of a journey.
    """
    origin = ""
    originId = ""

    destination = ""
    destinationId = ""

    transportLine = None
    lineDirection = ""

    plannedDeparture = None
    departureDelay = 0

    plannedArrival = None
    arrivalDelay = 0

    walking = False
    walkingDistance = 0

    def __init__(self, origin, destination, transportLine, plannedDeparture, plannedArrival,  lineDirection, walking):

        self.origin = origin
        self.destination = destination
        self.transportLine = transportLine
        self.lineDirection = lineDirection

        self.plannedDeparture = plannedDeparture
        self.plannedArrival = plannedArrival

        self.walking = walking

    def __str__(self):
        if self.walking:
            return self.origin + " -> " + self.destination
        else:
            return self.origin + " -> " + self.transportLine.name + " " + self.lineDirection + " -> " + self.destination


class Departure:
    """
    Contains information about a specific departure.
    """

    tripId = ""
    plannedWhen = ""
    delay = 0
    line = None
    direction = ""
    cancelled = False

    def __init__(self, tripId, plannedWhen, delay, line, direction):
        self.plannedWhen = plannedWhen
        self.tripId = tripId
        self.delay = delay
        self.line = line
        self.direction = direction

    def __str__(self):
        info = "{}  {}  {}".format(self.line.name, self.direction, getMinutesToDepartures(self.plannedWhen, self.delay))

        if self.cancelled:
            info = info + " CANCELLED"
        return info

class Station:
    """
    Contains information about a station.
    """

    stationId = ""
    name = ""
    products = list()
    lines = list()
    departures = list()

    def __init__(self, stationId):
        self.stationId = stationId
        self.getStationName()

    def __str__(self):
        return "{}: {} ".format(self.stationId, self.name)

    def getProducts(self):
        response = makeStopsRequest(self.stationId, Modes.STOPS_ID)

        if response.status_code == 200:
            parseStopsResponse(response.json(), Modes.STOPS_ID, self)
        else:
            print("Got invalid response\nstatus={}\n".format(response.status_code))

    def getLines(self):
        response = makeStationsRequest(self.stationId, Modes.STATIONS_ID)

        if response.status_code == 200:
            parseStationResponse(response.json(), self, Modes.STATIONS_ID)
        else:
            print("Got invalid response\nstatus={}\n".format(response.status_code))

    def getStationName(self):
        response = makeStopsRequest(self.stationId, Modes.STOPS_ID)

        if response.status_code == 200:
            self.name = response.json()["name"]
        else:
            print("Got invalid response\nstatus={}\n".format(response.status_code))

    def getDepartures(self, span=10):
        response = makeStopsRequest(self.stationId, Modes.STOPS_ID_DEPARTURES, span=span)

        if response.status_code == 200:
            parseStopsResponse(response.json(), Modes.STOPS_ID_DEPARTURES, self)
        else:
            print("Got invalid response\nstatus={}\n".format(response.status_code))

    def printFullInfo(self):
        print("{} ({})".format(self.name, self.stationId))

        for transportMode in self.products:
            print("{}: ".format(transportMode), end="")

            first = True

            for line in self.lines:
                if line.product == transportMode:
                    if first:
                        print(line.name, end="")
                        first = False
                    else:
                        print(", {}".format(line.name), end="")

            print("")


class Line:
    """
    Contains information about a line.
    """

    lineId = ""
    name = ""
    product = ""

    def __init__(self, lineId, name, product):
        self.lineId = lineId
        self.name = name
        self.product = product

    def __str__(self):
        return "{}: {} is a {}".format(self.lineId, self.name, self.product)


def fetchRequest(requestString, queryParams):
    """
    Sends the request.

    :param requestString: The base url with an endpoint
    :param queryParams: a dictionary containing optional query arguments
    :returns: a response for the request, or None on Error
    """

    response = None

    try:
        response = requests.get(requestString, queryParams)

        if DEBUG:
            print(response.url)

    except requests.exceptions.ConnectionError:
        print("Could not fetch {}".format(requestString))

    return response


def makeJourneyRequest(journeyObj, mode):

    data = None
    requestString = API_HOST + API_GET_JOURNEY

    if mode == Modes.JOURNEY_BY_ID:
        data = {"from": journeyObj.origin, "to": journeyObj.destination}

    return fetchRequest(requestString, data)


def makeStopsRequest(stopId, mode, span=10):
    """
    Makes a request string and parameters in order to fetch information from stops API endpoint. Makes the
    request via fetchRequest().

    :param stopId: The stop id to get information for.
    :param mode: The type of stop request to make.
    :param span: if mode is STOPS_ID_DEPARTURES, span is used to limit the departures for the next span minutes
    :return: Returns the fetched request.
    """

    data = None
    requestString = API_HOST + API_GET_STOPS

    if stopId is not str:
        stopIdStr = str(stopId)
    else:
        stopIdStr = stopId

    if mode == Modes.STOPS_ID:
        requestString += stopIdStr

    elif mode == Modes.STOPS_ID_DEPARTURES:
        requestString += stopIdStr + "/departures"

        if span != 10:
            data = {"duration": span}

    return fetchRequest(requestString, data)


def makeStationsRequest(stationId, mode, limit=3, fuzzy=False, completion=True):
    """
    Makes a request string and parameters in order to fetch information from station API endpoint. Makes the
    request via fetchRequest().

    :param stationId: The station id to get information for.
    :param mode: The type of station request to make.
    :param limit: (optional) limit the amount of stations returned by the API in a STATIONS_QUERY request.
    :param fuzzy: (optional) set to indicate possible typos in stationId by the API in a STATIONS_QUERY request.
    :param completion: (optional) set to indicate stationId to be not full name of a station in a STATIONS_QUERY request.
    :return: Returns the fetched request.
    """

    data = None
    requestString = API_HOST + API_GET_STATIONS

    if stationId is not str:
        stationStr = str(stationId)
    else:
        stationStr = stationId

    if mode == Modes.STATIONS_ID:
        requestString += "/" + stationStr
    elif mode == Modes.STATIONS_QUERY:
        data = {"query": stationStr}

        if limit != 3:
            data.update({"limit": limit})
        if fuzzy:
            data.update({"fuzzy": True})
        if not completion:
            data.update({"completion": False})

    return fetchRequest(requestString, data)


def parseStationResponse(response, station, mode):
    """
    Parses a station request.

    :param response: API station response to parse
    :param station: Station object to parse request into
    :param mode: type of information to parse
    :return:    None, if the response is empty, or mode is STATION_ID
                a list of station objects, if mode STATION_QUERY
    """

    dictItems = len(response)

    if not (type(response) is dict):
        print("response is not a dict")
        return None

    if dictItems == 0:
        print("Response is empty!")
        return None

    if mode == Modes.STATIONS_QUERY:
        # possible stations for query

        stations = list()

        for entry in response:
            result = response[entry]

            newStation = Station(result["id"])
            newStation.name = result["name"]
            stations.append(newStation)

        return stations

    elif mode == Modes.STATIONS_ID:
        # get further information about station: lines

        lines = response["lines"]

        for line in lines:
            addedLine = Line(line["id"], line["name"], line["product"])
            station.lines.append(addedLine)

        return


def parseStopsResponse(response, mode, station):
    """
    Parses a stop request.

    :param response: API stop response to parse
    :param station: Station object to parse request into
    :param mode: type of information to parse
    :return:    None, if the response is empty, or on other error
                    0 on success
    """

    dictItems = len(response)

    if dictItems == 0:
        print("Response is empty!")
        return None

    if mode == Modes.STOPS_ID:
        # parse products
        try:
            products = response["products"]
        except KeyError:
            print("Error: No products found in response!")
            return None

        for product in products:
            if products[product]:
                station.products.append(product)

    elif mode == Modes.STOPS_ID_DEPARTURES:

        for dep in response:

            lineResponse = dep["line"]
            newLine = Line(lineResponse["id"], lineResponse["name"], lineResponse["product"])

            newDeparture = Departure(dep["tripId"], dep["plannedWhen"], dep["delay"], newLine, dep["direction"])

            if "cancelled" in dep:
                newDeparture.cancelled = dep["cancelled"]

            station.departures.append(newDeparture)

    return 0

def parseJourneyResponse(response, connectionsObj, mode):
    """
    Parses a journey request.

    :param response: API journey response to parse
    :param connectionsObj: a connections object to store connection information into
    :param mode: type of information to parse
    :return: None
    """

    if mode == Modes.JOURNEY_BY_ID:
        # Parse possible connections between two stations, addressed by ID's

        journeys = response["journeys"]
        connectionsObj.routes = list()

        for j in journeys:

            journeyObj = Journey(connectionsObj.origin, connectionsObj.destination)
            journeyObj.legs = list()

            legs = j["legs"]

            for l in legs:

                line = None
                walking = False
                direction = ""

                if "walking" in l:

                    if l["origin"]["name"] == l["destination"]["name"]:
                        # filter out transfer on station
                        continue

                    walking = True
                else:
                    # "optional" responses that are not set when walking
                    line = Line(l["line"]["id"], l["line"]["name"], l["line"]["product"])
                    direction = l["direction"]

                newLeg = Leg(l["origin"]["name"], l["destination"]["name"], line, l["plannedDeparture"],
                             l["plannedArrival"],  direction, walking)

                if walking:
                    newLeg.walkingDistance = l["distance"]

                journeyObj.legs.append(newLeg)

            journeyObj.getTransfers()
            connectionsObj.routes.append(journeyObj)

    return


def getMinutesToDepartures(depTime, delay):
    """
    Calculates approximate minutes to a departure.
    :param depTime: ISO datetime string of the planned departure
    :param delay: the delay of a departure
    :return: amount of minutes to departure
    """

    if delay is None:
        delay = 0

    timeParsed = depTime[:-6]

    diff = datetime.datetime.fromisoformat(timeParsed) - datetime.datetime.now()
    diff_seconds = diff.total_seconds() + delay / 60

    return int(diff_seconds / 60)
