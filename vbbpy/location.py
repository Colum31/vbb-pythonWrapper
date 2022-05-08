from geopy.geocoders import Nominatim

class Address:

    addressStr = ""
    cords = None

    def getCords(self, inputStr):
        geolocator = Nominatim(user_agent="vbbpy: address lookup")
        location = geolocator.geocode(inputStr)

        self.addressStr = location.address
        self.cords = Coordinates(location.latitude, location.longitude)

    def __init__(self, inputStr):
        self.getCords(inputStr)

    def __str__(self):
        return self.addressStr + '\n' + str(self.cords)


class Coordinates:

    longitude = 0
    latitude = 0

    def __init__(self, lat, long):
        self.latitude = lat
        self.longitude = long

    def __str__(self):
        # this library only covers the vbb, so the coordinates will be
        # in the north-eastern hemisphere
        return "N{} E{}".format(self.longitude, self.latitude)
