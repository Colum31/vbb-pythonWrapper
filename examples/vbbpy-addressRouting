#!/usr/bin/env python3
"""
addressRouting - Get and show connections between two addresses. Uses OpenStreetMap API, so some places are also
recognized by their name.

Example script for vbb-pythonWrapper.
Author: Colum31
"""

import sys
from vbbpy import connections, location, vbbHelper


def addressLookup(addrStr):
    testAddr = location.Address(addrStr)

#   uncomment to get more details on address
#    print(testAddr)

    return testAddr


def main():

    if (len(sys.argv)) != 3:
        print("usage: {} [origin address] [destination address]\n\nIf the address or place contains a space, "
              "use quotation marks.\nExample: {} \"TU Berlin\" \"FU Berlin\"".format(sys.argv[0], sys.argv[0]))
        sys.exit(1)

    # sets user agent to identify
    vbbHelper.VbbHelper.setUserAgent("vbbpy: addressRouting example")

    # uncomment to show queried url
    # vbbHelper.VbbHelper.setDebug()

    origin = addressLookup(sys.argv[1])
    dest = addressLookup(sys.argv[2])

    testJourneys = connections.Connections(origin, dest)
    testJourneys.getConnections()

    for j in testJourneys.routes:
        print(j)

    return 0


if __name__ == "__main__":
    main()
