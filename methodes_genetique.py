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

#
nb_parents = 2

# Création de la liste de villes de façon aléatoire
cities = [city(i, random.randint(0, grid_size), random.randint(0, grid_size))for i in range(nb_cities)]



#################################################################################################
###########################  Génération des parents  ############################################
#################################################################################################

def generateParents(n, cities):
    numbers = list(range(nb_cities))
    tabParent = []
    for i in range(n):
        random.shuffle(numbers)
        listCities = []
        for j in numbers : 
            listCities.append(cities[j])
        tabParent.append(chemin(str(i), listCities))
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
    tabEnfants.append(chemin("0",halfP1))

    for i in parent1.cities :
        if (not(i in halfP2)) :
            halfP2.append(i)
    tabEnfants.append(chemin("1",halfP2))

    return tabEnfants

#################################################################################################
###########################  Fonction de sélection  #############################################
#################################################################################################
#? On cherche à maximiser le score de nos chemins
def select(tabEnfants, tabParents):
    scores = []
    scores.append(tabParents[0].score)
    scores.append(tabParents[1].score)
    scores.append(tabEnfants[0].score)
    scores.append(tabEnfants[1].score)

    scores.sort(reverse=True) # Ordre décroissant
    return scores[0], scores[1] # On retourne les deux scores maximaux
