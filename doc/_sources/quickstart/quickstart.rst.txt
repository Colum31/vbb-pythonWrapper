==================
Quick start guide
==================

Many of the examples here are embedded in own scripts, which you can find in the example folder.
You also can follow along within an interactive session.

Starting somewhere
==================

Journeys start from stations. Stations can be searched by their name, using the static function queryStations:

.. code-block:: python

    >>> from vbbpy.station import Station
    >>> list = Station.queryStations("Zoologischer Garten") # stationName is a string

This will return a list of stations, initialized and ready to use.
The station name does not need to be exact. The API will return up to 3 stations, that have the most familiar name.

If you want to initialize a station object by hand, you need its unique id. This id can be obtained by querying it.
You can then initialize it manually:

.. code-block:: python

    >>> from vbbpy.station import Station
    >>> demoStation = Station("900000023201") # id of "Zoologischer Garten"

You can print the information from a station with the usual print function:

.. code-block:: python

    >>> print(demoStation)
    900000023201: S+U Zoologischer Garten

This will print a stations name and id.

Starting from an address
========================

.. warning::

    You should check if the address is in Berlin / Brandenburg and valid before passing the object to any other function.


The vbb API requires the coordinates of an address to properly route. Luckily, we can use OpenStreetMaps to find the coordinates.
Addresses are stored in an address object (duh) and contain an coordinates object accordingly.

Similar to station querying, you pass a string containing the address in the constructor.

.. code-block:: python

    >>> from vbbpy import location
    >>> demoLocation = location.Address("TU Berlin")

You can also print it with print():

.. code-block:: python

    >>> print(demoLocation)
    Levetzowstraße
    10555 Berlin
    N13.326954140959668 E52.51101585


Getting a stations lines
========================

It might be useful to find out, which lines stop at a specific station.
To find that out, you need a initialized station object.

You then call two functions:

| getProducts()   - This will fetch which products are available (bus, subway, train etc.)
| getLines()      - This will fetch the lines of said products (245, U5, R1 ...)

You can then print the results using the printFullInfo() function.
Everything together:

.. code-block:: python

    >>> from vbbpy.station import Station
    >>> demoStation = Station("900000023201") # id of "Zoologischer Garten"
    >>> demoStation.getProducts()
    >>> demoStation.getLines()
    >>> demoStation.printFullInfo()
    S+U Zoologischer Garten (900000023201)
    suburban: S7, S7, S9, S5, S5, S3, S3, S3
    subway: U2, U3, U9
    bus: X10, M45, M46, M49, N2, X34, N10, 110, 200, N9, 245, N1, 109, 249, 204, 100, N26, 200, N7X, 204, A05, RB14
    express:
    regional: RE1, RE2, RE7, RB22, RB14, RB21

You can access the information in the station object.

| The products are stored in a the list "products" as strings.
| The lines are stored in the list "lines" as line objects.


Getting departures
==================

.. note::

    The departure times are being calculated with the current system time. If your machine time is set in another
    timezone, your departure times will be offset.

You can fetch information about upcoming departures via the function getDepartures(). You can supply the time limit as
a optional parameter.

.. code-block:: python

    >>> from vbbpy.station import Station
    >>> demoStation = Station("900000023201") # id of "Zoologischer Garten"
    >>> demoStation.getDepartures()

The departures are stored as departure object which can be printed by print():

.. code-block:: python

    >>> for dep in demoStation.departures:
    ...     print(dep)
    ...
    U2  U Theodor-Heuss-Platz  0
    S5  S Westkreuz  1
    109  Charlottenburg, Hertzallee  2
    M45  Spandau, Johannesstift  2
    U9  S+U Rathaus Steglitz  2
    ........

The time of the departure is displayed as rounded down minute ( 1:30 min to departure -> 1, 0:45 -> 0)
The delay is already accounted. Sometimes negative values might be displayed, if the departure time was in the past, but
the departure is still returned by the API (delay not accurate?).

All of the information is available in the departure object.


Routing
=======

The routing is made by the API. It returns possible routes between two addresses / stations .

Some terminology:
    - connections: The connections class holds information about possible routes ("journeys").
    - journey: A journey contains information about one possible route from start to endpoint. It contains of legs.
    - leg: A leg describes one part of a journey (taking a bus, walking ...)

In order to get routes, a connections object must be filled with information and then getConnections() called.

Origin and destination can be set by initializing a connections object:

.. code-block:: python

    >>> from vbbpy import connections
    >>> demoRoutes = connections.Connections(origin, dest)
    >>> demoRoutes.getConnections()


Where origin and dest can either be:
    - a station object
    - a stationId as a string
    - an address object

The connections object will now contain routes from origin to dest, stored as journeys. These journeys can be iterated
through and printed:

.. code-block:: python

    >>> for j in demoRoutes.routes:
    ...     print(j)
    ...


If you print the connections object itself, you will get an overview of the journeys.
