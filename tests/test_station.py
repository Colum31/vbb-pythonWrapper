from unittest import TestCase
from vbbpy import station, modes


class StationClass(TestCase):

    def test_parseStationRequest_emptyResponse(self):
        """
        Tests if parseStationRequests returns None, if the response is empty.

        :return: None
        """

        testStation = station.Station("", getName=False)
        testData = "{}"
        self.assertEqual(None, testStation.parseStationResponse(testData, None, modes.Modes.STATIONS_ID),
                         "expected to return None on empty response")
