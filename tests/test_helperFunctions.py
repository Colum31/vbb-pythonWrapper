from unittest import TestCase
from vbbpy import classes
import datetime


def gen_timestring(i):
    """
    Generate a dateTime string in the ISO8061 format, similar to the API.

    :param i: amount of offset minutes to add
    :return: datetime string
    """
    dtObj = datetime.datetime.now()
    dtObj = dtObj.replace(microsecond=0)

    # 5 seconds are added to offset test execution time
    dtObj = dtObj + datetime.timedelta(minutes=i, seconds=5)
    return dtObj.strftime("%Y-%m-%dT%H:%M:%S+02:00")


class HelperFunctions(TestCase):

    def test_hourMinuteString(self):
        """
        Tests if getDateTimeHourMinuteString returns correct string.

        :return: None
        """
        testData = {"2019-05-21T15:03:01+02:00": "15:03", "2019-05-21T15:03:01": "15:03",
                    "2020-11-23T01:31:01+02:00": "01:31", "2020-11-23T01:31:01": "01:31"}

        for data in testData.items():
            self.assertEqual(data[1], classes.getDateTimeHourMinuteString(data[0]),
                             "returned not correct hourMinute string!")

    def test_minutesToDepartures(self):
        """
        Tests if getMinutesToDepartures returns correct amount of minutes.
        Tests the delay functionality.

        :return: None
        """
        for i in range(20):
            self.assertEqual(i, classes.getMinutesToDepartures(gen_timestring(i), 0),
                             "returned wrong amount of minutes (without delay)")
            self.assertEqual(2 * i, classes.getMinutesToDepartures(gen_timestring(i), i * 60),
                             "returned wrong amount of minutes (with delay)")

    def test_parseStationRequest_emptyResponse(self):
        """
        Tests if parseStationRequests returns None, if the response is empty.

        :return: None
        """

        testData = "{}"
        self.assertEqual(None, classes.parseStationResponse(testData, None, classes.Modes.STATIONS_ID),
                         "expected to return None on empty response")
        self.assertEqual(None, classes.parseStationResponse(testData, None, classes.Modes.STATIONS_QUERY),
                         "expected to return None on empty response")

    def test_parseStationRequest_stationQuery_parse_id_name(self):
        """
        Tests if parseStationRequests correctly parses name and id of response in Query mode.

        :return: None
        """

        testSet1 = {"id": "12345", "name": "test1"}
        testSet2 = {"id": "67890", "name": "test2"}

        testSetComplete = {testSet1["id"]: testSet1, testSet2["id"]: testSet2}

        results = classes.parseStationResponse(testSetComplete, None, classes.Modes.STATIONS_QUERY)

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
