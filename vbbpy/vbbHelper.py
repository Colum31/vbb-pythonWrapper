import requests
import datetime

API_HOST = "https://v5.vbb.transport.rest/"
API_GET_STATIONS = "stations"
API_GET_STOPS = "stops/"
API_GET_JOURNEY = "journeys"
DEBUG = False
HEADER = {"User-Agent": "vbb-pythonWrapper (application not specified)"}


class VbbHelper:
    """
    A helper class for the library.
    """

    @staticmethod
    def setUserAgent(newUserAgent: str) -> None:
        """
        Sets the User Agent used when fetching the request.
        :param newUserAgent: New user agent to use
        :return: None
        """
        global HEADER
        HEADER = {"User-Agent": newUserAgent}

    @staticmethod
    def setDebug(to: bool = True) -> None:
        """
        Sets debug flag to specified state.
        :param to: state to set Debug to. By default, sets it to True.
        :return: None
        """
        global DEBUG
        DEBUG = to

    @staticmethod
    def fetchRequest(requestString: str, queryParams: dict):
        """
        Sends the request.

        :param requestString: The base url with an endpoint
        :param queryParams: a dictionary containing optional query arguments
        :returns: a response for the request, or None on Error
        """

        response = None

        try:
            response = requests.get(requestString, queryParams, headers=HEADER)

            if DEBUG:
                print(response.url)

        except requests.exceptions.ConnectionError:
            print("Could not fetch {}".format(requestString))

        return response

    @staticmethod
    def getMinutesToDepartures(depTime: str, delay: int) -> int:
        """
        Calculates approximate minutes to a departure.
        :param depTime: ISO datetime string of the planned departure
        :param delay: the delay of a departure
        :return: amount of minutes to departure
        """

        if delay is None:
            delay = 0

        timeParsed = depTime[:-6]

        diff = datetime.datetime.fromisoformat(timeParsed) - datetime.datetime.now()
        diff_seconds = diff.total_seconds() + delay

        return int(diff_seconds / 60)

    @staticmethod
    def getDateTimeHourMinuteString(dt: str, delay: int = 0) -> str:
        """
        Makes a string containing hour and minute of a given datetime.
        :param dt: datetime string to calculate string for
        :param delay: a possible delay (in seconds) to add to datetime before making the string
        :return: hh:mm formatted string of datetime time
        """

        if delay is None:
            delay = 0

        dtObj = datetime.datetime.fromisoformat(dt) + datetime.timedelta(seconds=delay)
        return dtObj.strftime("%H:%M")
