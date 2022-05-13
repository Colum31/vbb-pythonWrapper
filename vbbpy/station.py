from vbbpy import vbbHelper, modes, line, departure, location


class Station:
    """
    Contains information about a station.
    """

    stationId = ""
    name = ""
    products = list()
    lines = list()
    departures = list()
    position = None

    def __init__(self, stationId, getName=True):
        self.stationId = stationId

        if getName:
            self.getStationName()

    def __str__(self):
        return "{}: {} ".format(self.stationId, self.name)

    @staticmethod
    def queryStations(query):

        requestString = vbbHelper.API_HOST + vbbHelper.API_GET_STATIONS
        data = {"query": query, "fuzzy": True, "completion": True}

        response = vbbHelper.VbbHelper.fetchRequest(requestString, data).json()
        stations = list()

        for entry in response:
            result = response[entry]

            newStation = Station(result["id"], getName=False)
            newStation.name = result["name"]
            newStation.parseLocation(result.get("location"))
            stations.append(newStation)

        return stations

    def parseLocation(self, responseLoc):

        if responseLoc.get("type") != 'location':
            return

        self.position = location.Coordinates(responseLoc.get("latitude"), responseLoc.get("longitude"))

    def getProducts(self):
        response = self.makeStopsRequest(self.stationId, modes.Modes.STOPS_ID)

        if response.status_code == 200:
            self.parseStopsResponse(response.json(), modes.Modes.STOPS_ID, self)
        else:
            print("Got invalid response\nstatus={}\n".format(response.status_code))

    def getLines(self):
        response = self.makeStationsRequest(self.stationId, modes.Modes.STATIONS_ID)

        if response.status_code == 200:
            self.parseStationResponse(response.json(), self, modes.Modes.STATIONS_ID)
        else:
            print("Got invalid response\nstatus={}\n".format(response.status_code))

    def getStationName(self):
        response = self.makeStopsRequest(self.stationId, modes.Modes.STOPS_ID)

        if response.status_code == 200:

            resJson = response.json()

            self.name = resJson.get("name", "")
            self.parseLocation(resJson.get("location"))
        else:
            print("Got invalid response\nstatus={}\n".format(response.status_code))

    def getDepartures(self, span=10):
        response = self.makeStopsRequest(self.stationId, modes.Modes.STOPS_ID_DEPARTURES, span=span)

        if response.status_code == 200:
            self.parseStopsResponse(response.json(), modes.Modes.STOPS_ID_DEPARTURES, self)
        else:
            print("Got invalid response\nstatus={}\n".format(response.status_code))

    def printFullInfo(self):
        print("{} ({})".format(self.name, self.stationId))

        for transportMode in self.products:
            print("{}: ".format(transportMode), end="")

            first = True

            for availableLine in self.lines:
                if availableLine.product == transportMode:
                    if first:
                        print(availableLine.name, end="")
                        first = False
                    else:
                        print(", {}".format(availableLine.name), end="")

            print("")

    def makeStationsRequest(self, stationId, mode, limit=3, fuzzy=False, completion=True):
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
        requestString = vbbHelper.API_HOST + vbbHelper.API_GET_STATIONS

        if stationId is not str:
            stationStr = str(stationId)
        else:
            stationStr = stationId

        if mode == modes.Modes.STATIONS_ID:
            requestString += "/" + stationStr
        elif mode == modes.Modes.STATIONS_QUERY:
            data = {"query": stationStr}

            if limit != 3:
                data.update({"limit": limit})
            if fuzzy:
                data.update({"fuzzy": True})
            if not completion:
                data.update({"completion": False})

        return vbbHelper.VbbHelper.fetchRequest(requestString, data)

    def parseStationResponse(self, response, station, mode):
        """
        Parses a station request.

        :param response: API station response to parse
        :param station: Station object to parse request into
        :param mode: type of information to parse
        :return:    None, if the response is empty, or number of available lines
        """

        if not (type(response) is dict):
            print("response is not a dict")
            return None

        dictItems = len(response)

        if dictItems == 0:
            print("Response is empty!")
            return None

        if mode == modes.Modes.STATIONS_ID:
            # get further information about station: lines

            lines = response["lines"]

            for availableLine in lines:
                addedLine = line.Line(availableLine["id"], availableLine["name"], availableLine["product"])
                station.lines.append(addedLine)

            return len(station.lines)

    def makeStopsRequest(self, stopId, mode, span=10):
        """
        Makes a request string and parameters in order to fetch information from stops API endpoint. Makes the
        request via fetchRequest().

        :param stopId: The stop id to get information for.
        :param mode: The type of stop request to make.
        :param span: if mode is STOPS_ID_DEPARTURES, span is used to limit the departures for the next span minutes
        :return: Returns the fetched request.
        """

        data = None
        requestString = vbbHelper.API_HOST + vbbHelper.API_GET_STOPS

        if stopId is not str:
            stopIdStr = str(stopId)
        else:
            stopIdStr = stopId

        if mode == modes.Modes.STOPS_ID:
            requestString += stopIdStr

        elif mode == modes.Modes.STOPS_ID_DEPARTURES:
            requestString += stopIdStr + "/departures"

            if span != 10:
                data = {"duration": span}

        return vbbHelper.VbbHelper.fetchRequest(requestString, data)

    def parseStopsResponse(self, response, mode, station):
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

        if mode == modes.Modes.STOPS_ID:
            # parse products
            try:
                products = response["products"]
            except KeyError:
                print("Error: No products found in response!")
                return None

            for product in products:
                if products[product]:
                    station.products.append(product)

        elif mode == modes.Modes.STOPS_ID_DEPARTURES:

            for dep in response:

                lineResponse = dep["line"]
                newLine = line.Line(lineResponse["id"], lineResponse["name"], lineResponse["product"])

                newDeparture = departure.Departure(dep["tripId"], dep["plannedWhen"], dep["delay"], newLine,
                                                   dep["direction"])

                if "cancelled" in dep:
                    newDeparture.cancelled = dep["cancelled"]

                station.departures.append(newDeparture)

        return 0
