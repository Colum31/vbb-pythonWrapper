#!/usr/bin/env python3

# stationId - Return a station-id for a stop name string.
# Author Colum31, 24.2.2022

import requests
import sys

API_HOST = "http://v5.vbb.transport.rest/"
API_GET_STATIONS = "stations"

DEBUG = True


class Station:
    stationId = ""
    name = ""

    def __init__(self, stationId, name):
        self.stationId = stationId
        self.name = name

    def printInfo(self):
        print("{}: {} ".format(self.stationId, self.name))


def fetchRequest(requestString, queryParams):

    response = None

    try:
        response = requests.get(requestString, queryParams)

        if DEBUG:
            print(response.url)

    except requests.exceptions.ConnectionError:
        print("Could not fetch {}".format(requestString))

    return response


def makeStationsRequest(station, byID=False, limit=3, fuzzy=False, completion=True):

    data = None
    requestString = API_HOST + API_GET_STATIONS

    if station is not str:
        stationStr = str(station)
    else:
        stationStr = station

    if byID:
        requestString += "/" + stationStr
    else:
        data = {"query": stationStr}

        if limit != 3:
            data.update({"limit": limit})
        if fuzzy:
            data.update({"fuzzy": True})
        if not completion:
            data.update({"completion": False})

    return fetchRequest(requestString, data)


def parseStationResponse(response, mode="simple"):

    dictItems = len(response)

    if not (type(response) is dict):
        print("response is not a dict")
        return None

    if dictItems == 0:
        print("Response is empty!")
        return None

    if mode == "simple":

        stations = list()

        for entry in response:
            result = response[entry]

            newStation = Station(result["id"], result["name"])
            stations.append(newStation)

        return stations


def main():

    if(len(sys.argv)) != 2:
        print("usage: {} [Station name]".format(sys.argv[0]))
        sys.exit(1)

    apiResponse = makeStationsRequest(sys.argv[1],  limit=20, byID=False, fuzzy=True, completion=True)

    if apiResponse is None:
        return 1

    statusCode = apiResponse.status_code

    if statusCode == 200:
        print("Got valid response!\nstatus = 200\n")
    else:
        print("Got invalid response\nstatus={}\n".format(statusCode))
        return 1

    test = apiResponse.json()
    resultList = parseStationResponse(test)

    if resultList is None:
        return 1

    for result in resultList:
        result.printInfo()

    return 0


if __name__ == "__main__":
    main()
