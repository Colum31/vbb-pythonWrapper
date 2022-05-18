import requests
from vbbpy import modes, station, vbbHelper, journey, location


class Connections:
    """
    Holds information about multiple connections between origin and destination.
    """

    originStation = None
    destinationStation = None

    routes = None

    def __init__(self, origin, destination):

        if origin is station.Station:
            self.originStation = origin
        elif type(origin) is location.Address:
            self.originStation = origin
        else:
            self.originStation = station.Station(origin)

        if destination is station.Station:
            self.destinationStation = destination
        elif type(destination) is location.Address:
            self.destinationStation = destination
        else:
            self.destinationStation = station.Station(destination)

    def __str__(self):
        stationStr = "{} -> {} \n-----------------------------------------\n".format(self.originStation.name,
                                                                                     self.destinationStation.name)
        stationStr += "{} routes:\n".format(len(self.routes))

        allRoutesStr = ""

        for r in self.routes:
            routeStr = "[{}] -> [{}] ({}min): ".format(vbbHelper.VbbHelper.getDateTimeHourMinuteString(r.journeyStart),
                                                       vbbHelper.VbbHelper.getDateTimeHourMinuteString(r.journeyEnd),
                                                       r.journeyLength)
            for l in r.legs:
                mode = l.transportLine

                if mode is not None:
                    mode = mode.name
                else:
                    mode = "walking"

                routeStr += "{}, ".format(mode)

            routeStr = routeStr[:-2]
            allRoutesStr += routeStr + '\n'

        return stationStr + allRoutesStr

    def getConnections(self) -> None:
        """
        Gets routes between origin and destination that are stored in calling object.

        :return: None
        """

        response = self.makeJourneyRequest()

        if response.status_code == 200:
            self.parseJourneyResponse(response.json(), modes.Modes.JOURNEY_BY_ID)
        else:
            print("Got invalid response\nstatus={}\n".format(response.status_code))

    def makeJourneyRequest(self) -> requests.Response:
        """
        Makes a request string and parameters in order to fetch information from journey API endpoint. Makes the
        request via fetchRequest().

        :param mode: The type of request to make
        :return: Returns the fetched request.
        """

        data = {}
        requestString = vbbHelper.API_HOST + vbbHelper.API_GET_JOURNEY

        if type(self.originStation) is station.Station:
            data.update({"from": self.originStation.stationId})
        elif type(self.originStation) is location.Address:
            data.update({"from.latitude": self.originStation.cords.latitude})
            data.update({"from.longitude": self.originStation.cords.longitude})
            data.update({"from.address": self.originStation.streetName})

        if type(self.destinationStation) is station.Station:
            data.update({"to": self.destinationStation.stationId})
        elif type(self.destinationStation) is location.Address:
            data.update({"to.latitude": self.destinationStation.cords.latitude})
            data.update({"to.longitude": self.destinationStation.cords.longitude})
            data.update({"to.address": self.destinationStation.streetName})

        return vbbHelper.VbbHelper.fetchRequest(requestString, data)

    def parseJourneyResponse(self, response: dict, mode: modes.Modes) -> None:
        # TODO: split this function into journey and leg class member functions
        """
        Parses a journey request.

        :param response: API journey response to parse
        :param mode: type of information to parse
        :return: None
        """

        if mode == modes.Modes.JOURNEY_BY_ID:
            # Parse possible connections between two stations, addressed by ID's

            journeys = response["journeys"]
            self.routes = list()

            for j in journeys:

                newJourney = journey.Journey(self.originStation, self.destinationStation, j)
                self.routes.append(newJourney)

        return
