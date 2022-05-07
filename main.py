from vbbpy import connections, station

def getDeparturesFromStation(time):

    testStation = station.Station("")
    testStation.getProducts()
    testStation.getLines()

    testStation.printFullInfo()
    testStation.getDepartures(span=time)

    for dep in testStation.departures:
        print(dep)


def main():

    testJourneys = connections.Connections("", "")
    testJourneys.getConnections()

    for j in testJourneys.routes:
        print(j)

    return 0


main()
