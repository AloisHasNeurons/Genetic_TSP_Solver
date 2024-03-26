from City import City
from Population import Population
from Route import Route
from GeneticAlgorithm import GeneticAlgorithm
import matplotlib.pyplot as plt
from matplotlib import image as mpimpg
import numpy as np
import random

################################################
# Binôme : Aloïs VINCENT et Jean REESE
# Implémentation d'un algorithme génétique pour résoudre le problème du voyageur de commerces
################################################

#####################################
#!###### Création des villes ########
#####################################

#?                    x   y    Nom
city_list = [City(290,180, "Paris"),
                City(390,420, "Marseille"),
                City(380,320, "Lyon"),
                City(250,410, "Toulouse"),
                City(450,410, "Nice"),
                City(170,260, "Nantes"),
                City(340,410, "Montpellier"),
                City(460,200, "Strasbourg"),
                City(200,360, "Bordeaux"),
                City(310,100, "Lilles"),
                ]
# nb_cities = len(city_list)
# plt.scatter(city_list[:, 0], city_list[:, 1], color='red', marker='o', label='Villes')

nb_cities = len(city_list)

# Extraction des attributs des villes
names = [city.name for city in city_list]
x = [city.x for city in city_list]
y = [city.y for city in city_list]

#####################################
#!##### Création du graphique #######
#####################################
image = mpimpg.imread("map.jpg")
plt.imshow(image)
plt.scatter(x, y, c='red', marker='.')
for i, name in enumerate(names):
    plt.text(x[i]+5, y[i]+5, name, size = 'xx-small')
plt.show()

#####################################
#!#### Génération des parents #######
#####################################
#? A partir de la liste de villes, créer 10 chemins "parents"
#? Ordre aléatoire, mais la première ville doit également être la dernière du chemin

def generateParents(nb_parents) :
    # Initialisation 
    nb_cities = len(city_list)
    indexes = list((range(1,nb_cities)))
    populationParent = [None] * (nb_parents)

    for i in range(nb_parents):
        orderedList = [None] * (nb_cities+1)
        # On change l'ordre de remplissage
        random.shuffle(indexes)
        # Pour remplir un parent aléatoire
        for j in range(1,nb_cities) :
            orderedList[j] = city_list[indexes[j-1]]
        # La première et la dernière ville sont fixées
        orderedList[0] = city_list[0]
        orderedList[-1] = city_list[0]
        newRoute = Route(i, orderedList)
        # On ajoute ce parent à la population
        populationParent[i] = newRoute
    # On renvoie un tableau de n parents néo-formés
    return populationParent

gen0 = Population(city_list=city_list, routes=generateParents(10))
gen0.printPopulation()
best3gen0 = Population(city_list=city_list, routes=gen0.selectFittest(3))
best3gen0.printPopulation()
#####################################
#!########## Croisements ############
#####################################