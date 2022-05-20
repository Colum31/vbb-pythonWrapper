#!/usr/bin/env python3
"""
stationId - Fetch a station id by the station name.

Example script for vbb-pythonWrapper.
Author: Colum31
"""

import sys

from vbbpy import station, vbbHelper


def main():

    if(len(sys.argv)) != 2:
        print("usage: {} [Station name]\n\nIf the station name contains a space, use quotation marks.\nExample: {} "
              "\"Zoologischer Garten\"".format(sys.argv[0], sys.argv[0]))
        sys.exit(1)

    # sets user agent to identify
    vbbHelper.VbbHelper.setUserAgent("vbbpy: stationId example")

    # uncomment to show queried url
    # vbbHelper.VbbHelper.setDebug()

    resultList = station.Station.queryStations(sys.argv[1])

    if resultList is None:
        print("No stations found.")
        return 1

    for result in resultList:
        print(result)

    return 0


if __name__ == "__main__":
    main()
