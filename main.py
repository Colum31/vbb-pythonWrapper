from vbbpy import connections, station, location


def getDeparturesFromStation(time):
    testStation = station.Station("")
    testStation.getProducts()
    testStation.getLines()

    testStation.printFullInfo()
    testStation.getDepartures(span=time)

    for dep in testStation.departures:
        print(dep)


def addressLookup():
    testAddr = location.Address("")
    print(testAddr)


def main():
    #    testJourneys = connections.Connections("", "")
    #    testJourneys.getConnections()

    #    for j in testJourneys.routes:
    #        print(j)

    addressLookup()

    return 0


main()
