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

data_city = pd.read_csv(path)

# Ajout d'une colonne coordonnées, tuples de longitude, latitude
data_city["Coordinates"] = list(zip(data_city.Longitude, data_city.Latitude))
# Conversion de la colonne en Point(longitude, latitude)
data_city["Coordinates"] = data_city["Coordinates"].apply(Point)
# Conversion en GeoDataFrame, pour tracer sur une carte
gdf = gpd.GeoDataFrame(data_city, geometry="Coordinates")


# This should be the path to the downloaded countries shapefile.
shapefile_path = 'data/ne_110m_admin_0_countries/ne_110m_admin_0_countries.shp'

# Load the shapefile
countries_gdf = gpd.read_file(shapefile_path)

# Déterminer le CRS UTM approprié pour la France métropolitaine
# Note : Le CRS UTM pour la France métropolitaine est généralement la zone 31N
utm_crs = 'EPSG:32631'

# Reprojection en système de coordonnées projeté pour des calculs précis
countries_gdf_projected = countries_gdf.to_crs(utm_crs)

# Filtrer pour obtenir la France métropolitaine en utilisant les coordonnées projetées
france_mainland = countries_gdf_projected[
    (countries_gdf_projected['NAME'] == 'France') & 
    (countries_gdf_projected.geometry.centroid.x >= -5e5) &  # X coord in meters in UTM
    (countries_gdf_projected.geometry.centroid.x <= 1e6) &   # X coord in meters in UTM
    (countries_gdf_projected.geometry.centroid.y >= 4.5e6) &  # Y coord in meters in UTM
    (countries_gdf_projected.geometry.centroid.y <= 5.5e6)    # Y coord in meters in UTM
]

# Re-project to original CRS to display on a geographic map
france_mainland = france_mainland.to_crs(countries_gdf.crs)

# Vérifiez à nouveau si le GeoDataFrame est vide
if not france_mainland.empty:
    # Créez une figure et un axe pour le tracé
    fig, ax = plt.subplots(figsize=(10, 10))

    # Tracé de la France métropolitaine après le filtrage
    france_mainland.plot(ax=ax, color='lightblue', edgecolor='black')

    # Personnalisation du graphique
    ax.set_title('Carte de la France métropolitaine')
    ax.set_axis_off()  # Désactiver les axes pour une carte épurée

    # Afficher le graphique
    plt.show()
else:
    print('Le GeoDataFrame de la France métropolitaine est vide.')


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