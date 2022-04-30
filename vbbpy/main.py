from vbbpy import classes

def getDeparturesFromStation(time):

    testStation = classes.Station("")
    testStation.getProducts()
    testStation.getLines()

    testStation.printFullInfo()
    testStation.getDepartures(span=time)

    for dep in testStation.departures:
        print(dep)


def main():

    testJourneys = classes.Connections("", "")
    testJourneys.getConnections()

    for j in testJourneys.routes:
        print(j)

    return 0


main()
