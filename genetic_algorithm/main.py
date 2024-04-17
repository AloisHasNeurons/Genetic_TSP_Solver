from City import City
from GeneticAlgorithm import GeneticAlgorithm
import os
import numpy as np
import pandas as pd
import time
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
def dataProcessing(country, nb_cities):
    # Chemin d'accès à la liste des villes, selon l'OS
    if os.name == "nt" : # Windows
        path = "data\\worldcities.csv"
    else : # Unix
        path = "data/worldcities.csv"

    data_city = pd.read_csv(path)
    data_city = data_city[data_city['Country'] == country]
    # Ajout d'une colonne coordonnées, tuples de longitude, latitude
    data_city["Coordinates"] = list(zip(data_city.Longitude, data_city.Latitude))
    # Conversion de la colonne en Point(longitude, latitude)
    data_city["Coordinates"] = data_city["Coordinates"].apply(Point)
    # Conversion en GeoDataFrame, pour tracer sur une carte

    data_city = data_city.head(nb_cities)

    city_list = data_city.apply(lambda row: City(row['Longitude'], row['Latitude'], row['City']), axis=1).tolist()
    return city_list, data_city


#######################################################
#!####  Exécution de l'Algorithme génétique ###########
#!####            Depuis le GUI             ###########
#######################################################


def execute(nb_iterations, canvas, fig, gax, mutation_rate, population_size, country, root, nb_cities, pause) :
    city_list, data_city = dataProcessing(country, nb_cities)
    algo = GeneticAlgorithm(mutation_rate = 0.04, population_size = 100, city_list = city_list, country = country, data_city = data_city)
    for i in range(nb_iterations):
        algo.run()
        if (i % 5 == 0):  # Affichage toutes les 5 itérations
            print("Itération " + str(i))
        if(algo.pop.selectFittest(1) != algo.previous_best) : # Nouveau dessin que s'il sera différent
            gax = algo.drawBestRoutes(algo.pop, 1, gax)
            canvas.draw()
            root.update()  # Met à jour l'interface graphique
            time.sleep(pause)  # Ajoute une pause pour ralentir l'exécution, ajustez selon besoin
    print("Done!")
    #algo.pop.selectFittest(1).printPopulation()


#######################################################
#!####  Exécution de l'Algorithme génétique ###########
#!####            Depuis le main            ###########
#######################################################

def execute_main(mutation_rate, nb_cities, nb_iterations, population_size, country, pause): 
    city_list, data_city = dataProcessing(country, nb_cities)
    fig, gax = plt.subplots(figsize=(10,10))
    algo = GeneticAlgorithm(mutation_rate = mutation_rate,
                            population_size = population_size, 
                            city_list = city_list, 
                            country = country, 
                            data_city = data_city)
    for i in range(nb_iterations):
        algo.run()
        if(algo.pop.selectFittest(1) != algo.previous_best) : # Nouveau dessin que s'il sera différent
            gax = algo.drawBestRoutes(algo.pop, 1, gax)
            #? Garde le graphique ouvert lors de l'exécution du code
            fig.canvas.draw()
            plt.pause(pause) #Nombre de secondes d'affichage
        # Affichage toutes les 5 itérations
        if (i%5 == 0):
            print("Itération " + str(i))
    # Affichage à la fin de l'exécution
    print("Done!")
    #algo.pop.selectFittest(1).printPopulation()
    plt.show()

if __name__ == "__main__" :
    country = "France"
    city_list, data_city = dataProcessing(country, 15)
    execute_main(
            nb_iterations = 100,
            mutation_rate = 0.04,
            population_size = 100, 
            country = "France", 
            nb_cities = 15,
            pause = 0.01)

#TODO : interface graphique, pourquoi pas : affichage de graphiques (en R ?) pour les statistiques sur les scores de chaque itération
#TODO : barre de progression dans l'interface graphique 
