from City import City
from GeneticAlgorithm import GeneticAlgorithm
import os
import numpy as np
import pandas as pd
# Pour l'affichage des cartes :
from shapely.geometry import Point
import geopandas as gpd
import matplotlib.pyplot as plt

################################################
# Binôme : Aloïs VINCENT et Jean REESE
# Implémentation d'un algorithme génétique pour résoudre le problème du voyageur de commerces
################################################

####################################################
#!###### Création des villes et de la carte ########
####################################################
# Chemin d'accès à la liste des villes, selon l'OS
if os.name == "nt" : # Windows
    path = "data\\worldcities.csv"
else : # Unix
    path = "data/worldcities.csv"

#! Sélection du pays
country = "Finland"

data_city = pd.read_csv(path)
data_city = data_city[data_city['Country'] == country]
# Ajout d'une colonne coordonnées, tuples de longitude, latitude
data_city["Coordinates"] = list(zip(data_city.Longitude, data_city.Latitude))
# Conversion de la colonne en Point(longitude, latitude)
data_city["Coordinates"] = data_city["Coordinates"].apply(Point)
# Conversion en GeoDataFrame, pour tracer sur une carte

nb_cities = 18
data_city = data_city.head(nb_cities)

city_list = data_city.apply(lambda row: City(row['Longitude'], row['Latitude'], row['City']), axis=1).tolist()

#####################################
#!#### Algorithme génétioque ########
#####################################
#? A partir de la liste de villes, créer 20 chemins "parents"
# Initialisation de l'algorithme et de ses paramètres
algo = GeneticAlgorithm(mutation_rate = 0.04, population_size = 100, city_list = city_list, country = country, data_city = data_city)
nb_iterations = 100
for i in range(nb_iterations):
    algo.run()
    fig, gax = algo.drawBestRoutes(algo.pop, 1)
    #? Garde le graphique ouvert lors de l'exécution du code
    fig.canvas.draw()
    # Affichage toutes les 5 itérations
    if (i%5 == 0):
        print("Itération " + str(i))
    plt.pause(0.0001) #Nombre de secondes d'affichage
# Affichage à la fin de l'exécution
print("Done!")
algo.pop.selectFittest(1).printPopulation()
plt.show()
#TODO : interface graphique, pourquoi pas : affichage de graphiques (en R ?) pour les statistiques sur les scores de chaque itération
#TODO : barre de progression dans l'interface graphique 