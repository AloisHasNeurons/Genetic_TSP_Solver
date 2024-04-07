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

#####################################
#!###### Création des villes ########
#####################################
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
gdf = gpd.GeoDataFrame(data_city, geometry="Coordinates")
print(gdf.head())

# This should be the path to the downloaded countries shapefile.
if os.name == "nt" : # Windows
    shapefile_path = "data\\ne_10m_admin_0_map_units\\ne_10m_admin_0_map_units.shp"
else : # Unix
    shapefile_path = "data/ne_10m_admin_0_map_units/ne_10m_admin_0_map_units.shp"


# Load the shapefile
countries_gdf = gpd.read_file(shapefile_path)

# Sélection des données correspondantes au pays
country_subset = countries_gdf[countries_gdf['NAME'] == country]


fig, gax = plt.subplots(figsize=(10,10))


# Plot the country
country_subset.plot(ax=gax, edgecolor='black',color='white')
# Plot the cities
gdf.plot(ax=gax, color='red', alpha = 0.5)


gax.set_xlabel('longitude')
gax.set_ylabel('latitude')

# Kill the spines
gax.spines['top'].set_visible(False)
gax.spines['right'].set_visible(False)

# Label the cities
# for x, y, label in zip(gdf['Coordinates'].x, gdf['Coordinates'].y, gdf['City']):
#     gax.annotate(label, xy=(x,y), xytext=(4,4), textcoords='offset points')

plt.show()


#TODO : Remplacer city_list par les données de data_city
#TODO : Changer le calcul de distance dans l'algo, pour calculer à partir de la longitude/latitude
#?                    x   y    Nom
city_list =    [City(290,180, "Paris"),
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


#####################################
#!#### Génération des parents #######
#####################################
#? A partir de la liste de villes, créer 20 chemins "parents"
# Initialisation de l'algorithme et de ses paramètres
algo = GeneticAlgorithm(mutation_rate = 0.05, population_size = 20, city_list = city_list, nb_iterations = 25)
gen0 = algo.init_population()
#algo.iterate(gen0)

#TODO : interface graphique, pourquoi pas : affichage de graphiques (en R ?) pour les statistiques sur les scores de chaque itération