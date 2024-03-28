from Population import Population
from Route import Route
import random
import numpy as np
class GeneticAlgorithm:
    # Constructeur = Initialisation des paramètres de l'algo
    def __init__(self, mutation_rate, population_size, city_list):
        self.mutation_rate = mutation_rate
        self.population_size = population_size
        self.city_list = city_list
        self.nb_cities = len(city_list)

    # Génération de la population initiale : renvoie une population
    def init_population(self):
        #? Ordre aléatoire, mais la première ville doit également être la dernière du chemin
        # Initialisation 
        indexes = list((range(1,self.nb_cities)))
        population = [None] * (self.population_size)
        city_list = self.city_list

        for i in range(self.population_size):
            orderedList = [None] * (self.nb_cities+1)
            # On change l'ordre de remplissage
            random.shuffle(indexes)
            # Pour remplir un parent aléatoire
            for j in range(1,self.nb_cities) :
                orderedList[j] = city_list[indexes[j-1]]
            # La première et la dernière ville sont fixées
            orderedList[0] = city_list[0]
            orderedList[-1] = city_list[0]
            newRoute = Route(i, orderedList)
            # On ajoute ce parent à la population
            population[i] = newRoute
        # On renvoie un tableau de n parents néo-formés
        return Population(city_list = city_list, routes = population)

    # Cross Over
    def crossOver(self, chr1, chr2) :
        #On récupère les villes des deux parents
        crossed1 = chr1.cities
        crossed2 = chr2.cities
        #Réglage des parametres des cross-overs : le début (inclus) et la fin (exclus)
        start = random.randint(1,(self.nb_cities-1))
        end = random.randint(start+1,(self.nb_cities))
        size = end-start
        #Initialisation : rest seront ici les listes des valeurs uniques de chacune des listes
        seq1 = [None] * (size)
        seq2 = [None] * (size)
        rest1 = [None] * (size)
        rest2 = [None] * (size)
        #On extrait les séquences à échanger
        for i in range(size) :
            seq1[i] = crossed1[start+i]
            seq2[i] = crossed2[start+i]
        # Convertir les listes en ensembles pour obtenir les valeurs uniques
        set_seq1 = set(map(tuple, seq1))
        set_seq2 = set(map(tuple, seq2))
        # Trouver les valeurs uniques dans chaque séquence
        unique_seq1 = set_seq1.difference(set_seq2)
        unique_seq2 = set_seq2.difference(set_seq1)
        # Convertir les ensembles de tuples en listes de arrays
        rest1 = [np.array(item) for item in unique_seq1]
        rest2 = [np.array(item) for item in unique_seq2]
        #On remplace les valeurs possiblement redondantes
        compteur = 0
        for i in range(self.nb_cities) :
            if np.any(np.all(crossed1[i] == rest2, axis=1)) :
                crossed1[i] = rest1[compteur]
                compteur = compteur + 1
        compteur = 0
        for i in range(self.nb_cities) :
            if np.any(np.all(crossed2[i] == rest1, axis=1)) :
                crossed2[i] = rest2[compteur]
                compteur = compteur + 1
        #On échange les deux portions !
        for i in range(size) :
            crossed1[start+i] = seq2[i]
            crossed2[start+i] = seq1[i]
        #On retourne les valeurs
        return [crossed1, crossed2]
        


#! Prometteur : mais ne fonctionne pas !! 
#? C'est trop optimiste, ici Paris n'est plus le point de départ, et le chemin ne se referme pas sur la première ville
    def crossOver2(self, papa, maman):
        #Réglage des parametres des cross-overs : le début (inclus) et la fin (exclus)
        start = random.randint(1,(self.nb_cities-1))
        end = random.randint(start+1,(self.nb_cities))

        # On prend tous les éléments de l'un, jusqu'au start, puis tous les éléments de l'autre entre
        # start et end, et on finit en prenant tous les éléments du premier à partir de la fin 
        child1_cities = papa.cities[:start] + maman.cities[start:end] + papa.cities[end:]
        child2_cities = maman.cities[:start] + papa.cities[start:end] + maman.cities[end:]

        child1_cities = self.rmDupCO(child1_cities, start, end)
        child2_cities = self.rmDupCO(child2_cities, start, end)
        return Route("Enfant 1", child1_cities), Route("Enfant 2", child2_cities)


    def rmDupCO(self, cities, start, end):
        #? Fonction qui retire les doublons pendant un crossing over
        unique_cities_order = []
        explored = set()
          
        # On s'assure de conserver l'ordre de la séquence échangée
        unique_cities_order.extend(cities[start:end])
        explored.update(cities[start:end])
        for city in cities[:start] + cities[end:]:
            if city not in explored:
                unique_cities_order.append(city)
                explored.add(city)
        return unique_cities_order