from vbbpy import connections, station, location


def getDeparturesFromStation(time):
    testStation = station.Station("")
    testStation.getProducts()
    testStation.getLines()

    testStation.printFullInfo()
    testStation.getDepartures(span=time)

    for dep in testStation.departures:
        print(dep)


def addressLookup(addrStr):
    testAddr = location.Address(addrStr)
    print(testAddr)

    return testAddr


def main():

    origin = addressLookup("")
    dest = addressLookup("")

    testJourneys = connections.Connections(origin, dest)
    testJourneys.getConnections()

    for j in testJourneys.routes:
        print(j)


    return 0


main()
