from chemin import chemin
from city import city
import numpy as np
import random
import matplotlib.pyplot as plt

#TODO :
# Interface graphique :
### On pourra rentrer le nombre de villes dans l'interface
### La grille se calculerait en fonction du nombre de villes
# Affichage des chemins en temps réél lors du calcul
# Donner de vrais noms de villes existantes qu'on piocherait dans un tableau par exemple


#! Nommage : 
## Un individu (parent ou enfant) = un chemin solution, de taille nb_cities
## Une population = un ensemble de chemins solution
## Taille de la population = nombre de parents à évaluer en simultané

#################################################################################################
###########################  Initialisation  ####################################################
#################################################################################################

# Nombre de villes = taille des individus
nb_cities = 10

# Taille de la grille   
grid_size = 100

#
nb_parents = 2

# Création de la liste de villes de façon aléatoire
cities = [city(i, random.randint(0, grid_size), random.randint(0, grid_size))for i in range(nb_cities)]


#################################################################################################
###########################  Affichages des villes  #############################################
#################################################################################################

# Affichage de la liste de villes dans la console
for i in cities:
    print(i.toString())

# Extraction des attributs des villes
names = [city.name for city in cities]
xs = [city.x for city in cities]
ys = [city.y for city in cities]

# Création d'un graphique
plt.ion
plt.scatter(xs, ys, c='red', marker='.')
# Annotations
for i, name in enumerate(names):
    plt.text(xs[i], ys[i], name)
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Carte des villes générées aléatoirement')
#? Garde le graphique ouvert lors de l'exécution du code
plt.show(block = False)


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
###########################  Affichage des parents  #############################################
#################################################################################################

#? Test de la génération des parents -> affichage console
tabParents = generateParents(nb_parents, cities)
for i in range(len(tabParents)):
    chemin = tabParents[i].cities
    print("\nParent " + str(i) + " Score :" + str(tabParents[i].score))
    # for j in chemin:
    #     print(j.toString())

#? Tracer le chemin des parents sur le graphique
#TODO : transformer en fonction
# Pour chaque ligne du tableau de parents
def tracerChemin(tabParents):
    for i in range(len(tabParents)):
        colors = ['red','blue','green','purple','pink']
        #On va tracer le chemin
        chemin = tabParents[i].cities
        for j in range((nb_cities-1)):
            plt.plot([chemin[j].x, chemin[j+1].x], [chemin[j].y, chemin[j+1].y], color = colors[i])
 
tracerChemin(tabParents)

plt.ioff()
plt.show()
plt.pause(0)

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
    #? on garde la première moitié des parents
    for i in range(half) :
        halfP1.append(parent1.cities[i])
        halfP2.append(parent2.cities[i])

    #? on prend chaque élément restant de l'autre parent, s'il n'est pas déjà dans la liste
    for i in parent2.cities :
        if (not(i in halfP1)) :
            halfP1.append(i)
    tabEnfants[0] = halfP1

    for i in parent1.cities :
        if (not(i in halfP2)) :
            halfP2.append(i)
    tabEnfants[1] = halfP2
    return tabEnfants


genEnfants(tabParents[0], tabParents[1])

#################################################################################################
###########################  Fonction de sélection  #############################################
#################################################################################################
#? On cherche à maximiser le score de nos chemins
def select(tabEnfants, tabParents) :
    if (tabEnfants[0].score > tabEnfants[1].score) :
        e1 = True
    if (tabParents[0].score > tabParents[1].score) : 
        p1 = True
    if (e1 == p1 == True) :
        return (tabEnfants[0], tabParents[0])
    elif () 