#!/usr/bin/env python3
"""
showDepartures - Show next departures from a station. Time is shown as rounded down minutes to departure.

Example script for vbb-pythonWrapper.
Author: Colum31
"""

import sys
from vbbpy import station


def getDeparturesFromStation(idString, time=10):
    testStation = station.Station(idString)

#    uncomment to print also station information
#    testStation.getProducts()
#    testStation.getLines()

#    testStation.printFullInfo()
    testStation.getDepartures(span=time)

    print("{} ({}): Departures for the next {} minutes:".format(testStation.name, testStation.stationId, time))
    print("-----------------------------------------------------------------------------------")

    for dep in testStation.departures:
        print(dep)

    print("-----------------------------------------------------------------------------------")


def main():
    if not (len(sys.argv) == 2 or len(sys.argv) == 3):
        print("usage: {} [station id] (optional: time limit)".format(sys.argv[0]))
        sys.exit(1)

    # Parse optional time limit. Default value is 10 minutes.
    if len(sys.argv) == 3:
        getDeparturesFromStation(sys.argv[1], time=int(sys.argv[2]))
    else:
        getDeparturesFromStation(sys.argv[1])
    return 0


if __name__ == "__main__":
    main()
