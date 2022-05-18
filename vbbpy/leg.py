import datetime

from vbbpy import vbbHelper, line

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

    invalidLeg = False

    def __init__(self, legDict: dict):

        if "walking" in legDict:

            if legDict.get("origin").get("id") == legDict.get("destination").get("id"):
                # filter out transfer on station, by setting invalid flag
                self.invalidLeg = True
                return

            self.origin = legDict.get("origin").get("name") or legDict.get("origin").get("address", "")
            self.destination = legDict.get("destination").get("name") or legDict.get("destination").get("address", "")

            self.transportLine = None

            self.walkingDistance = legDict.get("distance", -1)
            self.walking = True
        else:
            # "optional" responses that are not set when walking
            self.transportLine = line.Line(legDict.get("line").get("id"), legDict.get("line").get("name"),
                                           legDict.get("line").get("product"))

            self.origin = legDict.get("origin").get("name")
            self.destination = legDict.get("destination").get("name")
            self.walking = False

        self.lineDirection = legDict.get("direction", "")
        self.arrivalDelay = int(legDict.get("arrivalDelay", "0") or 0)
        self.departureDelay = int(legDict.get("departureDelay", "0") or 0)
        self.plannedDeparture = legDict.get("plannedDeparture")
        self.plannedArrival = legDict.get("plannedArrival")

        self.setTimeDuration()

    def __str__(self):

        depStr = "[{}] {} -> ".format(vbbHelper.VbbHelper.getDateTimeHourMinuteString(self.plannedDeparture, self.departureDelay), self.origin)
        arrStr = " -> [{}] {}".format(vbbHelper.VbbHelper.getDateTimeHourMinuteString(self.plannedArrival, self.arrivalDelay), self.destination)

        if self.walking:

            walkStr = "{}m".format(self.walkingDistance)
            return depStr + walkStr + arrStr
        else:

            lineStr = "{} {}".format(self.transportLine.name, self.lineDirection)
            return depStr + lineStr + arrStr

    def setTimeDuration(self) -> None:
        """
        Calculates and sets time required for the leg.

        :return: None
        """

        diff = datetime.datetime.fromisoformat(self.plannedArrival) - datetime.datetime.fromisoformat(self.plannedDeparture)
        diff_seconds = diff.total_seconds()

        if not ((self.arrivalDelay is None) or (self.departureDelay is None)):
            diff_seconds += self.arrivalDelay - self.departureDelay

        self.timeDurationMinutes = int(diff_seconds / 60)
