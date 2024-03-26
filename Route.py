from City import City
import numpy as np
class Route :
    def __init__(self, name, cities):
        self.name = str(name)
        self.cities = cities
        self.score = self.evaluate()
    
    #? Distance euclidienne entre deux villes
    def distance(self, city1, city2):
        return np.sqrt((city1.x - city2.x)**2 + (city1.y - city2.y)**2)

    #? Attribution du score basé sur la distance, on cherche à minimiser le score
    def evaluate(self):
        score = 0
        for i in range(len(self.cities) - 1):
            score += self.distance(self.cities[i], self.cities[i+1])
        return round(score, 2)

    def containsCity(self, item) : 
        return item in self.cities
    
    def toString(self) :
        result = "Route " + self.name + " (score = " + str(self.score) +") :\n"
        for city in self.cities : 
            result += city.toString() 
        return result