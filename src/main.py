import classes

def main():

    testStation = classes.Station("")
    testStation.getProducts()
    testStation.getLines()

    testStation.printFullInfo()
    testStation.getDepartures(span=60)

    for dep in testStation.departures:
        print(dep)

    return 0


main()
