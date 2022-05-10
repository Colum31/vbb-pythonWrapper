from geopy.geocoders import Nominatim

class Address:

    name = ""
    streetName = ""
    number = 0
    postalCode = 0
    city = ""

    cords = None

    def getCords(self, inputStr):
        geolocator = Nominatim(user_agent="vbbpy: address lookup")
        loc = geolocator.geocode(inputStr, addressdetails=True)

        self.name = loc.address
        self.cords = Coordinates(loc.latitude, loc.longitude)

        addressData = loc.raw.get('address')

        self.streetName = addressData.get('road', "")
        self.number = addressData.get("house_number", "")
        self.postalCode = addressData.get("postcode", "")
        self.city = addressData.get("city", "")

    def __init__(self, inputStr):
        self.getCords(inputStr)

    def __str__(self):
        return self.streetName + " " + self.number + '\n' + self.postalCode + " " + self.city + '\n' + str(self.cords)


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
