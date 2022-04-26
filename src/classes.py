import requests
import enum

DEBUG = True


class Modes(enum.Enum):
    STATIONS_QUERY = 0
    STATIONS_ID = 1
    STOPS_ID = 2
    STOPS_ID_DEPARTURES = 3


class Station:
    stationId = ""
    name = ""
    products = list()
    lines = list()

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
    lineId = ""
    name = ""
    product = ""

    def __init__(self, lineId, name, product):
        self.lineId = lineId
        self.name = name
        self.product = product

    def __str__(self):
        return "{}: {} is a {}".format(self.lineId, self.name, self.product)



API_HOST = "http://v5.vbb.transport.rest/"
API_GET_STATIONS = "stations"
API_GET_STOPS = "stops/"


'''
Sends the request.
'''


def fetchRequest(requestString, queryParams):
    response = None

    try:
        response = requests.get(requestString, queryParams)

        if DEBUG:
            print(response.url)

    except requests.exceptions.ConnectionError:
        print("Could not fetch {}".format(requestString))

    return response


'''
Makes a request string and parameters in order to fetch information from stops API endpoint.
'''


def makeStopsRequest(stopId, mode):
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

    return fetchRequest(requestString, data)


'''
Makes a request string and parameters in order to fetch information from stations API endpoint.
'''


def makeStationsRequest(station, mode, limit=3, fuzzy=False, completion=True):
    data = None
    requestString = API_HOST + API_GET_STATIONS

    if station is not str:
        stationStr = str(station)
    else:
        stationStr = station

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


'''
Parses requests of stations endpoint
'''


def parseStationResponse(response, station, mode):
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

            newStation = Station(result["id"], result["name"])
            stations.append(newStation)

        return stations

    elif mode == Modes.STATIONS_ID:
        # get further information about station: lines

        lines = response["lines"]

        for line in lines:
            addedLine = Line(line["id"], line["name"], line["product"])
            station.lines.append(addedLine)

        return


'''
Parses requests of stops endpoint
'''


def parseStopsResponse(response, mode, station):
    if mode == Modes.STOPS_ID:
        # parse products
        try:
            products = response["products"]
        except KeyError:
            print("Error: No products found in response!")
            return

        for product in products:
            if products[product]:
                station.products.append(product)
        return
