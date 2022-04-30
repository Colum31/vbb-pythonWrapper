#!/usr/bin/env python3

# stationId - Return a station-id for a stop name string.
# Author Colum31, 24.2.2022

import sys
from vbbpy import classes
from vbbpy.classes import Modes


def main():

    if(len(sys.argv)) != 2:
        print("usage: {} [Station name]".format(sys.argv[0]))
        sys.exit(1)

    apiResponse = classes.makeStationsRequest(sys.argv[1], Modes.STATIONS_QUERY, fuzzy=True, completion=True)
    resultList = classes.parseStationResponse(apiResponse.json(), None, Modes.STATIONS_QUERY)

    if resultList is None:
        return 1

    for result in resultList:
        print(result)

    return 0


if __name__ == "__main__":
    main()
