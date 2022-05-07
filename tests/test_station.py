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
        self.assertEqual(None, testStation.parseStationResponse(testData, None, modes.Modes.STATIONS_QUERY),
                         "expected to return None on empty response")

    def test_parseStationRequest_stationQuery_parse_id_name(self):
        """
        Tests if parseStationRequests correctly parses name and id of response in Query mode.

        :return: None
        """

        testSet1 = {"id": "12345", "name": "test1"}
        testSet2 = {"id": "67890", "name": "test2"}

        testStation = station.Station("", getName=False)

        testSetComplete = {testSet1["id"]: testSet1, testSet2["id"]: testSet2}

        results = testStation.parseStationResponse(testSetComplete, None, modes.Modes.STATIONS_QUERY)

        if type(results) is not list:
            self.fail("Expected to return a list")

        self.assertEqual(len(testSetComplete), len(results), "Expected to have as many results as test data sets")

        for result in results:

            resId = result.stationId
            name = result.name

            dataSet = testSetComplete.get(resId)

            if dataSet is None:
                self.fail("Did not find data in test set")

            if dataSet["id"] is not resId:
                self.fail("rid of data does not match test data")

            if dataSet["name"] is not name:
                self.fail("name of data does not match test data")

            testSetComplete.pop(resId)
