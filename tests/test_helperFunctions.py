import datetime
from unittest import TestCase

from vbbpy import vbbHelper


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
            self.assertEqual(data[1], vbbHelper.VbbHelper.getDateTimeHourMinuteString(data[0]),
                             "returned not correct hourMinute string!")

    def test_minutesToDepartures(self):
        """
        Tests if getMinutesToDepartures returns correct amount of minutes.
        Tests the delay functionality.

        :return: None
        """
        for i in range(20):
            self.assertEqual(i, vbbHelper.VbbHelper.getMinutesToDepartures(gen_timestring(i), 0),
                             "returned wrong amount of minutes (without delay)")
            self.assertEqual(2 * i, vbbHelper.VbbHelper.getMinutesToDepartures(gen_timestring(i), i * 60),
                             "returned wrong amount of minutes (with delay)")
