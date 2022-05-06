#!/usr/bin/env python3

# stationId - Return a station-id for a stop name string.
# Author Colum31, 24.2.2022

import sys
from station import Station

def main():

    if(len(sys.argv)) != 2:
        print("usage: {} [Station name]".format(sys.argv[0]))
        sys.exit(1)

    resultList = Station.queryStations(sys.argv[1])

    if resultList is None:
        return 1

    for result in resultList:
        print(result)

    return 0


if __name__ == "__main__":
    main()
