import enum


class Modes(enum.Enum):
    """
    Enum of modes to indicate a operation type.
    """

    STATIONS_QUERY = 0
    STATIONS_ID = 1

    STOPS_ID = 2
    STOPS_ID_DEPARTURES = 3

    JOURNEY_BY_ID = 4
