from Chemin import Chemin
from City import City
import numpy as np
import random


#################################################################################################
########################  Initialisation des paramètres  ########################################
#################################################################################################


# Nombre de villes = taille des individus
try:
    nb_cities = int(input("Nombre de villes : "))
except ValueError:
    nb_cities = 20  # Default value

# Taille de la grille   
try:
    grid_size = int(input("Taille de la grille : "))
except ValueError:
    grid_size = 100  # Default value

try:
    nb_iterations = int(input("Nombre d'itérations : "))
except ValueError:
    nb_iterations = 10  # Default value

# Strictement supérieur à 1 
nb_parents = 2

# Création de la liste de villes de façon aléatoire
cities = [City(i, random.randint(0, grid_size), random.randint(0, grid_size))for i in range(nb_cities)]
# TODO : faire des villes prédéfinies


#################################################################################################
###########################  Génération des parents  ############################################
#################################################################################################

def generateParents(n, cities):
    numbers = list(range(1,nb_cities))
    tabParent = []
    for i in range(n):
        random.shuffle(numbers)
        listCities = [cities[0]]
        for j in numbers : 
            listCities.append(cities[j])
        listCities.append(listCities[0])
        tabParent.append(Chemin(str(i), listCities))

    # while (tabParent[0] == tabParent[1]):
    #     random.shuffle(numbers)
    #     for j in numbers : 
    #         listCities.append(cities[j])
    #     listCities.append(listCities[0])
    #     tabParent[1] = (Chemin(str(i), listCities))

    return tabParent


#################################################################################################
###########################  Génération des enfants  ############################################
#################################################################################################

# def rmDup(cities):
#     exploredNames = []
#     explored = []
#     for city in cities :
#         if not(city.name in explored) :
#             exploredNames.append(city.name)
#             explored.append(city)
#     return cities

# #! Une façon de faire parmi tant d'autres : peut-être pas la plus efficace
# # On coupe la séquence parent en 2, puis on remplit le reste de la séquence avec les villes
# # de l'autre parent, qui ne sont pas déjà présentes, dans l'ordre
# def genEnfants(parent1, parent2):
#     half = int(len(parent1.cities)/2)
#     halfP1 = []
#     halfP2 = []
#     tabEnfants = []
#     #? on garde la première moitié des parents
#     for i in range(half) :
#         halfP1.append(parent1.cities[i])
#         halfP2.append(parent2.cities[i])

#     #? on prend chaque élément restant de l'autre parent, s'il n'est pas déjà dans la liste
#     for i in parent2.cities :
#         if (not(i in halfP1)) :
#             halfP1.append(i)
#     halfP1 = rmDup(halfP1)
#     halfP1.append(halfP1[0])
#     tabEnfants.append(Chemin("0",halfP1))

#     for i in parent1.cities :
#         if (not(i in halfP2)) :
#             halfP2.append(i)
#     halfP2 = rmDup(halfP2)
#     halfP2.append(halfP2[0])
#     tabEnfants.append(Chemin("1",halfP2))
#     return tabEnfants

#! tenter de faire d'une autre façon : prendre un couple de sommets sur 2
#! mieux : intervertir un segment entre deux indices au hasard, 
# ex de chemin[2] à chemin[6],
# à ce moment-là les deux parents garderaient chemin[0] et chemin[1], 
# auraient le segment 2-6 de l'autre, et garderaient leur chemin[>6]

# #! pb d'index out of range parfois à régler
# def genEnfants2(parent1, parent2):
#     size = len(parent1.cities)-1
#     x = random.randrange(size-1)    
#     y = random.randrange(x+1, size)
#     newP1 = []
#     newP2 = []

#     for i in range(0, x) :
#         newP1.append(parent1.cities[i])
#         newP2.append(parent2.cities[i])
#     for i in range(x, y+1) :
#         newP1.append(parent2.cities[i])
#         newP2.append(parent1.cities[i])
#     for i in range(y+1, len(parent1.cities)) :
#         newP1.append(parent1.cities[i])
#         newP2.append(parent2.cities[i])
    
#     tabEnfants = [Chemin("1", newP1), Chemin("2", newP2)]
#     return tabEnfants

def crossoverPMX(parent1, parent2):
    size = len(parent1.cities) - 1  # On retire 1 pour ne pas inclure la ville dupliquée dans le calcul
    child = [None] * size  # Initialisation de l'enfant sans la ville dupliquée
    
    # Sélectionner deux points de croisement au hasard
    point1, point2 = sorted(random.sample(range(size), 2))
    
    # Copier le segment du parent1 vers l'enfant
    for i in range(point1, point2 + 1):
        child[i] = parent1.cities[i]
    
    # Remplir le reste avec les villes du parent2, en respectant l'ordre et l'unicité
    current_index = 0  # On commence à remplir depuis le début de child
    for city in parent2.cities[:-1]:  # Ignorer la dernière ville de parent2 car elle est dupliquée
        if city not in child:
            # Trouver le prochain emplacement libre dans child
            while child[current_index] is not None:
                current_index += 1
            child[current_index] = city
    
    # Ajouter la ville de départ à la fin pour compléter le circuit
    child.append(child[0])
    
    return [Chemin("Enfant", child)]



#################################################################################################
###########################  Fonction de mutation  #############################################
#################################################################################################
#? On fait un test aléatoire par rapport au taux de mutation et en cas de mutation on inverse l'ordre de i et i+1
# TODO : rajouter des nouveaux types de mutations : écriture dans l'autre sens, déplacement
def mutate(parent, mutation_rate):
    cities = parent.cities[:-1] # Ignorer la ville de retour au début pour la mutation
    for i in range(len(cities)):
        if random.random() < mutation_rate:
            j = random.randint(0, len(cities)-1)
            cities[i], cities[j] = cities[j], cities[i]
    return [parent.cities[0]] + cities + [parent.cities[0]] # Ajouter la ville de départ/retour

            



#################################################################################################
###########################  Fonction de sélection  #############################################
#################################################################################################
#? On cherche à minimiser le score de nos chemins
def select(tabEnfants, tabParents):
    scores = []
    scores.append((tabParents[0].score, tabParents[0]))
    scores.append((tabParents[1].score, tabParents[1]))
    scores.append((tabEnfants[0].score, tabEnfants[0]))
    #scores.append((tabEnfants[1].score, tabEnfants[1]))
    # On classe par ordre croissant sur le score
    scores.sort(key=lambda x: x[0])
    # On retourne les meilleurs chemins   
    return [scores[0][1], scores[1][1]] 
