from Population import Population
from Route import Route
import random
import numpy as np
class GeneticAlgorithm:
    # Constructeur = Initialisation des paramètres de l'algo
    def __init__(self, mutation_rate, population_size, city_list, nb_iterations):
        self.mutation_rate = mutation_rate
        self.population_size = population_size
        self.city_list = city_list
        self.nb_cities = len(city_list)
        self.nb_iterations = nb_iterations

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
    #! NE FONCTIONNE PAS 
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
        set_seq1 = set(seq1)
        set_seq2 = set(seq2)
        # Trouver les valeurs uniques dans chaque séquence
        unique_seq1 = set_seq1.difference(set_seq2)
        unique_seq2 = set_seq2.difference(set_seq1)
        # Convertir les ensembles de tuples en listes de arrays
        rest1 = [np.array(item) for item in unique_seq1]
        rest2 = [np.array(item) for item in unique_seq2]
        #On remplace les valeurs possiblement redondantes
        compteur = 0
        for i in range(self.nb_cities) :
            if np.any(np.all(crossed1[i] == rest2, axis=0)) :
                crossed1[i] = rest1[compteur]
                compteur = compteur + 1
        compteur = 0
        for i in range(self.nb_cities) :
            if np.any(np.all(crossed2[i] == rest1, axis=0)) :
                crossed2[i] = rest2[compteur]
                compteur = compteur + 1
        #On échange les deux portions !
        for i in range(size) :
            crossed1[start+i] = seq2[i]
            crossed2[start+i] = seq1[i]
        #On retourne les valeurs
        return Route("Child 1", crossed1), Route("Child 2", crossed2)

    def mutate(self, population):
        for i in range(len(population.routes)):
            for j in range(1, self.nb_cities) :
                if random.random() < self.mutation_rate:
                    x = random.rand(0, 1)
                    if x == 0 :
                        population.routes[j] = self.fullReverse(population=population, position = j)
                    if x == 1 :
                        population.routes[j] = self.partReverse(population=population, position = j)
                    #TODO : Rajouter d'autres types de mutations 

    def fullReverse(self, population, position):
        cities = population.routes[position].cities
        rev = [None] * len(cities)
        for i in range(len(cities)):
            rev[i] = cities[-(i+1)]
        return Route(name = population[position].name, cities=rev)

    def partReverse(self, population, position) :
        cities = population.routes[position].cities
        x = random.randint(1, len(cities)-1)
        partRev = cities[:x] + cities[x + 2] + cities[x + 1] + cities[x+3:]
        return Route(partRev)