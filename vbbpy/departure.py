from vbbHelper import VbbHelper

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
        info = "{}  {}  {}".format(self.line.name, self.direction, VbbHelper.getMinutesToDepartures(self.plannedWhen, self.delay))

        if self.cancelled:
            info = info + " CANCELLED"
        return info
