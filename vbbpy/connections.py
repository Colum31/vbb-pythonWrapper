from vbbpy import line, modes, station, leg, vbbHelper, journey

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
        else:
            self.originStation = station.Station(origin)

        if destination is station.Station:
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
                                                       vbbHelper.VbbHelper.getDateTimeHourMinuteString(r.journeyEnd), r.journeyLength)

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

    def getConnections(self):
        response = self.makeJourneyRequest(modes.Modes.JOURNEY_BY_ID)

        if response.status_code == 200:
            self.parseJourneyResponse(response.json(), modes.Modes.JOURNEY_BY_ID)
        else:
            print("Got invalid response\nstatus={}\n".format(response.status_code))

    def makeJourneyRequest(self, mode):
        """
        Makes a request string and parameters in order to fetch information from journey API endpoint. Makes the
        request via fetchRequest().

        :param mode: The type of request to make
        :return: Returns the fetched request.
        """

        data = None
        requestString = vbbHelper.API_HOST + vbbHelper.API_GET_JOURNEY

        if mode == modes.Modes.JOURNEY_BY_ID:
            data = {"from": self.originStation.stationId, "to": self.destinationStation.stationId}

        return vbbHelper.VbbHelper.fetchRequest(requestString, data)

    def parseJourneyResponse(self, response, mode):
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

                journeyObj = journey.Journey(self.originStation.stationId,
                                     self.destinationStation.stationId)
                journeyObj.legs = list()

                journeyObj.originStation = self.originStation
                journeyObj.destinationStation = self.destinationStation

                legs = j["legs"]

                for l in legs:

                    lineObj = None
                    walking = False
                    direction = ""

                    arrivalDelay = 0
                    departureDelay = 0

                    if "walking" in l:

                        if l["origin"]["id"] == l["destination"]["id"]:
                            # filter out transfer on station
                            continue

                        walking = True
                    else:
                        # "optional" responses that are not set when walking
                        lineObj = line.Line(l["line"]["id"], l["line"]["name"], l["line"]["product"])
                        direction = l["direction"]
                        arrivalDelay = int(l["arrivalDelay"] or 0)
                        departureDelay = int(l["departureDelay"] or 0)

                    newLeg = leg.Leg(l["origin"]["name"], l["destination"]["name"], lineObj, l["plannedDeparture"],
                                     l["plannedArrival"], direction, walking)

                    newLeg.departureDelay = departureDelay
                    newLeg.arrivalDelay = arrivalDelay

                    if walking:
                        newLeg.walkingDistance = l["distance"]

                    newLeg.setTimeDuration()
                    journeyObj.legs.append(newLeg)

                journeyObj.getTransfers()
                journeyObj.getTimeInfo()
                self.routes.append(journeyObj)

        return
