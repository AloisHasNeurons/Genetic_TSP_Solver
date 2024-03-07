from chemin import chemin
from city import city
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
    grid_size = 10  # Default value

# Strictement supérieur à 1 
nb_parents = 2

# Création de la liste de villes de façon aléatoire
cities = [city(i, random.randint(0, grid_size), random.randint(0, grid_size))for i in range(nb_cities)]



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
        tabParent.append(chemin(str(i), listCities))

    while (tabParent[0] == tabParent[1]):
        random.shuffle(numbers)
        for j in numbers : 
            listCities.append(cities[j])
        listCities.append(listCities[0])
        tabParent[1] = (chemin(str(i), listCities))

    return tabParent


#################################################################################################
###########################  Génération des enfants  ############################################
#################################################################################################

#! Une façon de faire parmi tant d'autres : peut-être pas la plus efficace
# On coupe la séquence parent en 2, puis on remplit le reste de la séquence avec les villes
# de l'autre parent, qui ne sont pas déjà présentes, dans l'ordre
def genEnfants(parent1, parent2):
    half = int(len(parent1.cities)/2)
    halfP1 = []
    halfP2 = []
    tabEnfants = []
    #? on garde la première moitié des parents
    for i in range(half) :
        halfP1.append(parent1.cities[i])
        halfP2.append(parent2.cities[i])

    #? on prend chaque élément restant de l'autre parent, s'il n'est pas déjà dans la liste
    for i in parent2.cities :
        if (not(i in halfP1)) :
            halfP1.append(i)
    halfP1.append(halfP1[0])
    tabEnfants.append(chemin("0",halfP1))

    for i in parent1.cities :
        if (not(i in halfP2)) :
            halfP2.append(i)
    halfP2.append(halfP2[0])
    tabEnfants.append(chemin("1",halfP2))

    return tabEnfants


#! tenter de faire d'une autre façon : prendre un couple de sommets sur 2
#! mieux : intervertir un segment entre deux indices au hasard, ex de chemin[2] à chemin[6],
# à ce moment-là les deux parents garderaient chemin[0] et chemin[1], auraient le segment 2-6 de l'autre,
# et garderaient leur chemin[>6]


#################################################################################################
###########################  Fonction de sélection  #############################################
#################################################################################################
#? On cherche à maximiser le score de nos chemins
def select(tabEnfants, tabParents):
    scores = []
    scores.append((tabParents[0].score, tabParents[0]))
    scores.append((tabParents[1].score, tabParents[1]))
    scores.append((tabEnfants[0].score, tabEnfants[0]))
    scores.append((tabEnfants[1].score, tabEnfants[1]))
    # On classe par ordre décroissant sur le score
    scores.sort(key=lambda x: x[0], reverse=True) 
    # On retourne les meilleurs chemins   
    return [scores[0][1], scores[1][1]] 