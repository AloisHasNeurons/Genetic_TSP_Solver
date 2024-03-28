from City import City
from Population import Population
from Route import Route
from GeneticAlgorithm import GeneticAlgorithm
import matplotlib.pyplot as plt
from matplotlib import image as mpimpg
import numpy as np


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
#? A partir de la liste de villes, créer 20 chemins "parents"

algo = GeneticAlgorithm(mutation_rate = 0.05, population_size = 20, city_list = city_list)
gen0 = algo.init_population()
# gen0.printPopulation()
best2gen0 = Population(city_list=city_list, routes=gen0.selectFittest(2))
best2gen0.printPopulation()

#####################################
#!########## Croisements ############
#####################################

#crossOver1et2 = crossOver(populationParent[1], populationParent[2])
enfant1, enfant2 = algo.crossOver2(best2gen0.routes[0], best2gen0.routes[1])
print(enfant1.toString())
print(enfant2.toString())