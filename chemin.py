from city import city
import numpy as np
class chemin(city):
    def __init__(self, name, cities):
        self.name = name
        self.cities = cities
        self.score = self.evaluate()

    #? Distance euclidienne entre deux villes
    def distance(self, city1, city2):
        return np.sqrt((city1.x - city2.x)**2 + (city1.y - city2.y)**2)


    #? Attribution du score basé sur la distance, on cherche à maximiser le score
    def evaluate(self):
        score = 0
        for i in range(cities.length()-1):
            for j in range(start = 1, stop = cities.length()-1):
                score += self.distance(cities[i], cities[y])
        score = np.log(score)
        return score
            