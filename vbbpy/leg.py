import datetime

from vbbpy import vbbHelper

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

    timeDurationMinutes = 0

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

        depStr = "[{}] {} -> ".format(vbbHelper.VbbHelper.getDateTimeHourMinuteString(self.plannedDeparture, self.departureDelay), self.origin)
        arrStr = " -> [{}] {}".format(vbbHelper.VbbHelper.getDateTimeHourMinuteString(self.plannedArrival, self.arrivalDelay), self.destination)

        if self.walking:

            walkStr = "{}m".format(self.walkingDistance)
            return depStr + walkStr + arrStr
        else:

            lineStr = "{} {}".format(self.transportLine.name, self.lineDirection)
            return depStr + lineStr + arrStr

    def setTimeDuration(self):

        diff = datetime.datetime.fromisoformat(self.plannedArrival) - datetime.datetime.fromisoformat(self.plannedDeparture)
        diff_seconds = diff.total_seconds()

        if not ((self.arrivalDelay is None) or (self.departureDelay is None)):
            diff_seconds += self.arrivalDelay - self.departureDelay

        self.timeDurationMinutes = int(diff_seconds / 60)
