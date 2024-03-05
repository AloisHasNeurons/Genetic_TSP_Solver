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
nb_cities = 30

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
        listTest = []
        for j in numbers : 
            listTest.append(cities[j])
        tabParent.append(chemin(str(i), listTest))
    return tabParent

#################################################################################################
###########################  Affichage des parents  #############################################
#################################################################################################

#? Test de la génération des parents -> affichage console
tabParents = generateParents(nb_parents, cities)
for i in range(len(tabParents)):
    chemin = tabParents[i].cities
    print("\nParent " + str(i) + " :" + str(tabParents[i].score))
    # for j in chemin:
    #     print(j.toString())

#? Tracer le chemin des parents sur le graphique
#TODO : transformer en fonction
# Pour chaque ligne du tableau de parents
for i in range(len(tabParents)):
    colors = ['red','blue','green','purple','pink']
    #On va tracer le chemin
    chemin = tabParents[i].cities
    for j in range((nb_cities-1)):
        plt.plot([chemin[j].x, chemin[j+1].x], [chemin[j].y, chemin[j+1].y], color = colors[i])
 

plt.ioff()
plt.show()
plt.pause(0)