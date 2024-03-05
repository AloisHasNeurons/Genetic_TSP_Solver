from city import city
import numpy as np
class chemin(city):
    def __init__(self, name, cities):
        self.name = name
        self.cities = cities
        self.score = self.evaluate(cities)

    #? Distance euclidienne entre deux villes
    def distance(self, city1, city2):
        return np.sqrt((city1.x - city2.x)**2 + (city1.y - city2.y)**2)


    #? Attribution du score basé sur la distance, on cherche à maximiser le score
    #TODO : maximiser le score avec une formule 
    def evaluate(self, cities):
        score = 0
        for i in range(len(cities)-1):
            for j in range(1, len(cities)-1):
                score += self.distance(cities[i], cities[j])
        return score
            