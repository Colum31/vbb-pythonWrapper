from connections import Connections
from station import Station

def getDeparturesFromStation(time):

    testStation = Station("")
    testStation.getProducts()
    testStation.getLines()

    testStation.printFullInfo()
    testStation.getDepartures(span=time)

    for dep in testStation.departures:
        print(dep)


def main():

    testJourneys = Connections("", "")
    testJourneys.getConnections()

    for j in testJourneys.routes:
        print(j)

    return 0


main()
