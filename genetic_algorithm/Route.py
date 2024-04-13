import math
class Route :
    def __init__(self, name, cities):
        self.name = str(name)
        self.cities = cities
        self.score = self.evaluate() # Distance totale en km
    
    # Calcul de la distance entre deux villes en utilisant la formule de Haversine.
    def haversine(self, city1, city2):
        # Rayon de la Terre en kilomètres
        R = 6371.0
        lat1, lon1 = city1.latitude, city1.longitude
        lat2, lon2 = city2.latitude, city2.longitude
        # Conversion des degrés en radians
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        
        # Différences de coordonnées
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        # Formule de Haversine
        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        # Distance en kilomètres
        distance = R * c
        return distance

    def evaluate(self):
        total_dist = 0
        for i in range(len(self.cities) - 1):
            total_dist += self.haversine(self.cities[i], self.cities[i+1])
        return round(total_dist, 2)

    def containsCity(self, item) : 
        return item in self.cities
    
    def toString(self) :
        result = "Route " + self.name + " (score = " + str(self.score) +"km ) :\n"
        for city in self.cities : 
            result += city.toString() 
        return result