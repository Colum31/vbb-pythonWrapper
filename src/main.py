import json
import requests
import classes
import enum

API_HOST = "http://v5.vbb.transport.rest/"
API_GET_STATIONS = "stations"
API_GET_STOPS = "stops/"


class Modes(enum.Enum):
    STATIONS_QUERY = 0
    STATIONS_ID = 1
    STOPS_ID = 2
    STOPS_ID_DEPARTURES = 3


DEBUG = True

'''
Sends the request.
'''
def fetchRequest(requestString, queryParams):
    response = None

    try:
        response = requests.get(requestString, queryParams)

        if DEBUG:
            print(response.url)

    except requests.exceptions.ConnectionError:
        print("Could not fetch {}".format(requestString))

    return response


'''
Makes a request string and parameters in order to fetch information from stops API endpoint.
'''
def makeStopsRequest(stopId, mode):
    data = None
    requestString = API_HOST + API_GET_STOPS

    if stopId is not str:
        stopIdStr = str(stopId)
    else:
        stopIdStr = stopId

    if mode == Modes.STOPS_ID:
        requestString += stopIdStr

    elif mode == Modes.STOPS_ID_DEPARTURES:
        requestString += stopIdStr + "/departures"

    return fetchRequest(requestString, data)


'''
Makes a request string and parameters in order to fetch information from stations API endpoint.
'''
def makeStationsRequest(station, mode, limit=3, fuzzy=False, completion=True):
    data = None
    requestString = API_HOST + API_GET_STATIONS

    if station is not str:
        stationStr = str(station)
    else:
        stationStr = station

    if mode == Modes.STATIONS_ID:
        requestString += "/" + stationStr
    elif mode == Modes.STATIONS_QUERY:
        data = {"query": stationStr}

        if limit != 3:
            data.update({"limit": limit})
        if fuzzy:
            data.update({"fuzzy": True})
        if not completion:
            data.update({"completion": False})

    return fetchRequest(requestString, data)


'''
Parses requests of stations endpoint
'''
def parseStationResponse(response, station, mode):
    dictItems = len(response)

    if not (type(response) is dict):
        print("response is not a dict")
        return None

    if dictItems == 0:
        print("Response is empty!")
        return None

    if mode == Modes.STATIONS_QUERY:
        # possible stations for query

        stations = list()

        for entry in response:
            result = response[entry]

            newStation = classes.Station(result["id"], result["name"])
            stations.append(newStation)

        return stations

    elif mode == Modes.STATIONS_ID:

        lines = response["lines"]

        for line in lines:
            addedLine = classes.Line(line["id"], line["name"], line["product"])
            station.lines.append(addedLine)

        return


'''
Parses requests of stops endpoint
'''
def parseStopsResponse(response, mode, station):
    if mode == Modes.STOPS_ID:
        # parse products
        try:
            products = response["products"]
        except KeyError:
            print("Error: No products found in response!")
            return

        for product in products:
            if products[product]:
                station.products.append(product)
        return


def main():
    apiResponse = makeStationsRequest("900000002201", Modes.STATIONS_ID)

    if apiResponse is None:
        return 1

    statusCode = apiResponse.status_code

    if statusCode == 200:
        print("Got valid response!\nstatus = 200\n")
    else:
        print("Got invalid respone\nstatus={}\n".format(statusCode))
        return 1

#    jsonString = json.dumps(apiResponse.json(), indent=4)
#    print(jsonString)
#    test = apiResponse.json()

    testStation = classes.Station("900000023201")
    testStation.getProducts()
    testStation.getLines()

    testStation.printFullInfo()

    return 0


main()
