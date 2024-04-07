from City import City
from GeneticAlgorithm import GeneticAlgorithm
# Pour l'affichage des cartes :
from shapely.geometry import Point
import pandas as pd
import geopandas as gpd
import os
import matplotlib.pyplot as plt
import numpy as np

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
country = "Italy"

data_city = pd.read_csv(path)
data_city = data_city[data_city['Country'] == country]
# Ajout d'une colonne coordonnées, tuples de longitude, latitude
data_city["Coordinates"] = list(zip(data_city.Longitude, data_city.Latitude))
# Conversion de la colonne en Point(longitude, latitude)
data_city["Coordinates"] = data_city["Coordinates"].apply(Point)
# Conversion en GeoDataFrame, pour tracer sur une carte

nb_cities = 20
data_city = data_city.head(nb_cities)


city_list = data_city.apply(lambda row: City(row['Longitude'], row['Latitude'], row['City']), axis=1).tolist()

#####################################
#!#### Algorithme génétioque ########
#####################################
#? A partir de la liste de villes, créer 20 chemins "parents"
# Initialisation de l'algorithme et de ses paramètres
algo = GeneticAlgorithm(mutation_rate = 0.05, population_size = 50, city_list = city_list, nb_iterations = 25, country = country, data_city = data_city)
gen0 = algo.init_population()
algo.iterate(gen0)

#TODO : interface graphique, pourquoi pas : affichage de graphiques (en R ?) pour les statistiques sur les scores de chaque itération