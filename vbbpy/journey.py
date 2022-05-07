import datetime
from math import ceil

from vbbpy import vbbHelper, modes, leg, line


class Journey:
    """
    Holds information about a single connection between origin and destination.
    """

    # TODO:
    # - refreshing Details?

    originStation = None
    destinationStation = None

    legs = None
    numberTransfers = 0

    journeyLength = 0
    journeyStart = ""
    journeyEnd = ""

    def __init__(self, origin, destination):
        self.originStation = origin
        self.destinationStation = destination

    def __str__(self):
        stationStr = "{} -> {} \n-----------------------------------------\n".format(self.originStation.name,
                                                                                     self.destinationStation.name)
        journeyString = "{} -> {} ({} min), {} transit(s)\n".format(vbbHelper.VbbHelper.getDateTimeHourMinuteString(self.journeyStart),
                                                                    vbbHelper.VbbHelper.getDateTimeHourMinuteString(self.journeyEnd),
                                                                    self.journeyLength, self.numberTransfers)

        for l in self.legs:
            journeyString += str(l) + '\n'

        return stationStr + journeyString

    def getTransfers(self):
        self.numberTransfers = len(self.legs) - 1

    def getTimeInfo(self):
        firstLeg = self.legs[0]
        lastLeg = self.legs[-1]

        journeyStartDt = datetime.datetime.fromisoformat(firstLeg.plannedDeparture) + datetime.timedelta(
            seconds=firstLeg.departureDelay)
        self.journeyStart = journeyStartDt.isoformat()

        journeyEndDt = datetime.datetime.fromisoformat(lastLeg.plannedArrival) + datetime.timedelta(
            seconds=lastLeg.arrivalDelay)
        self.journeyEnd = journeyEndDt.isoformat()

        journeyLengthTd = journeyEndDt - journeyStartDt
        self.journeyLength = int(ceil(journeyLengthTd.total_seconds() / 60))

    def makeJourneyRequest(self, connectionsObj, mode):
        """
        Makes a request string and parameters in order to fetch information from journey API endpoint. Makes the
        request via fetchRequest().

        :param connectionsObj: A connections object to get start and endpoint from
        :param mode: The type of request to make
        :return: Returns the fetched request.
        """

        data = None
        requestString = vbbHelper.API_HOST + vbbHelper.API_GET_JOURNEY

        if mode == modes.Modes.JOURNEY_BY_ID:
            data = {"from": connectionsObj.originStation.stationId, "to": connectionsObj.destinationStation.stationId}

        return vbbHelper.VbbHelper.fetchRequest(requestString, data)

    def parseJourneyResponse(self, response, connectionsObj, mode):
        """
        Parses a journey request.

        :param response: API journey response to parse
        :param connectionsObj: a connections object to store connection information into
        :param mode: type of information to parse
        :return: None
        """

        if mode == modes.Modes.JOURNEY_BY_ID:
            # Parse possible connections between two stations, addressed by ID's

            journeys = response["journeys"]
            connectionsObj.routes = list()

            for j in journeys:

                journeyObj = Journey(connectionsObj.originStation.stationId,
                                     connectionsObj.destinationStation.stationId)
                journeyObj.legs = list()

                journeyObj.originStation = connectionsObj.originStation
                journeyObj.destinationStation = connectionsObj.destinationStation

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
                connectionsObj.routes.append(journeyObj)

        return
