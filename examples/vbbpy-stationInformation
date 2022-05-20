#!/usr/bin/env python3
"""
stationInformation - Get station name and available lines / products from a station id.

Example script for vbb-pythonWrapper.
Author: Colum31
"""

from vbbpy import station, vbbHelper
import sys

def getInformation(idString):
    testStation = station.Station(idString)
    testStation.getProducts()
    testStation.getLines()
    testStation.printFullInfo()


def main():

    if not len(sys.argv) == 2:
        print("usage: {} [station id]".format(sys.argv[0]))
        sys.exit(1)

    # sets user agent to identify
    vbbHelper.VbbHelper.setUserAgent("vbbpy: stationInformation example")

    # uncomment to show queried url
    # vbbHelper.VbbHelper.setDebug()

    getInformation(sys.argv[1])

    return 0


if __name__ == "__main__":
    main()
