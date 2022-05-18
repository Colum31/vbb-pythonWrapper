import datetime
from math import ceil

from vbbpy import vbbHelper, leg


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

    def __init__(self, origin, destination, journeyDict: dict):
        self.originStation = origin
        self.destinationStation = destination

        inputLegList = journeyDict.get("legs", list())
        self.legs = list()

        for rawLeg in inputLegList:

            nextLeg = leg.Leg(rawLeg)

            if not nextLeg.invalidLeg:
                self.legs.append(nextLeg)

        # calculate transfers and length of journey
        self.getTransfers()
        self.getTimeInfo()

    def __str__(self):
        stationStr = "{} -> {} \n-----------------------------------------\n".format(self.originStation.name,
                                                                                     self.destinationStation.name)
        journeyString = "{} -> {} ({} min), {} transit(s)\n".format(vbbHelper.VbbHelper.getDateTimeHourMinuteString(self.journeyStart),
                                                                    vbbHelper.VbbHelper.getDateTimeHourMinuteString(self.journeyEnd),
                                                                    self.journeyLength, self.numberTransfers)

        for l in self.legs:
            journeyString += str(l) + '\n'

        return stationStr + journeyString

    def getTransfers(self) -> None:
        """
        Gets the amount of transfers and stores them in the calling object.

        :return:
        """
        self.numberTransfers = len(self.legs) - 1

    def getTimeInfo(self) -> None:
        """
        Gets the length of the journey in minutes and stores it into calling object.

        :return: None
        """

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
