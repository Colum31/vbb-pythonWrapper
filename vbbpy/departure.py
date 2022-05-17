from vbbpy import vbbHelper, line

class Departure:
    """
    Contains information about a specific departure.
    """

    tripId = ""
    plannedWhen = ""
    delay = 0
    depLine = None
    direction = ""
    cancelled = False

    def __init__(self, tripId: str, plannedWhen: str, delay: int, depLine: line.Line, direction: str):
        self.plannedWhen = plannedWhen
        self.tripId = tripId
        self.delay = delay
        self.depLine = depLine
        self.direction = direction

    def __str__(self):
        info = "{}  {}  {}".format(self.depLine.name, self.direction, vbbHelper.VbbHelper.getMinutesToDepartures(self.plannedWhen, self.delay))

        if self.cancelled:
            info = info + " CANCELLED"
        return info
