class City :
    def __init__(self, longitude, latitude, name):
        self.longitude = longitude
        self.latitude = latitude
        self.name = str(name)

    def toString(self):
        return ("Longitude : "+ str(self.longitude) + " | Latitude : " + str(self.latitude) + " | Name : " + str(self.name) + "\n")

    