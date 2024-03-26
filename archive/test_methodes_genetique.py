from chemin import chemin
from city import city
import numpy as np
import random
import unittest

def genEnfants(parent1, parent2):
    # Implement the logic to generate children here
    children = parent1.cities + parent2.cities
    return [
        chemin("0", children),
        chemin("1", children)
    ]

class TestGenEnfants(unittest.TestCase):
    nb_cities = 10
    grname_size = 100  # Default value
    nb_iterations = 10  # Default value
    nb_parents = 2

    cities = [city(i, random.randint(0, 100), random.randint(0, 100))for i in range(10)]
    def test_genEnfants(self):
        parent1 = chemin("0", [city for city in self.cities])
        parent2 = chemin("1", [city for city in self.cities])
        
        expected = [
            chemin("0", [city for city in self.cities] + [city for city in self.cities]),
            chemin("1", [city for city in self.cities] + [city for city in self.cities])
        ]
        
        result = genEnfants(parent1, parent2)
        
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()