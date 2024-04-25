from .City import City
from .GeneticAlgorithm import GeneticAlgorithm
import os
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


def execute(nb_iterations, canvas, fig, gax, mutation_rate, population_size, 
            country, root, nb_cities, pause, progress_callback, stats_callback,
            nb_routes, stop_callback) :
    # Formattage des donnéees pour correspondre au pays sélectionné
    city_list, data_city = dataProcessing(country, nb_cities)
    # Création d'une instance de l'algo avec les paramètres
    algo = GeneticAlgorithm(mutation_rate=mutation_rate, population_size = population_size, city_list = city_list, country = country, data_city = data_city)
    #  Création des listes pour les graphiques de statistiques
    best_list = []
    average_list = []
    # Création des variables des conditions d'arrêt
    no_improvement_counter = 0
    best_solution = float('inf')
    # Boucle de n itérations :
    for i in range(nb_iterations):
        # Produit une itération de l'algo
        algo.run(nb_routes)

        #! Mise à jour du dessin
        if (algo.pop.selectFittest(nb_routes) != algo.previous_best) : # Nouveau dessin que s'il sera différent
            gax = algo.drawBestRoutes(algo.pop, nb_routes, gax)
            canvas.draw()
            root.update()  # Met à jour l'interface graphique
            time.sleep(pause)  # Ajoute une pause pour ralentir l'exécution

        #! Création des variables de statistiques, renvoi vers l'interface graphique
        best, average = algo.pop.statsDistance()
        best_list.append(best)
        average_list.append(average)
        stats_callback(best = round(best, 2), average = round(average, 2))

        #! Conditions d'arrêt :
        if best < best_solution:
            best_solution = best
            no_improvement_counter = 0
        else:
            no_improvement_counter += 1
        if no_improvement_counter >= 200:  #? On arrête si le meilleur chemin ne change pas pendant 100 itérations
            print("No improvement for 200 iterations, stopping at iteration " + str(i))
            stop_callback("No improvement for 200 iterations, stopping at iteration " + str(i))
            break
        #? On arrête également si la moyenne de la pop == le meilleur chemin 
        if round(best, 2) == round(average,2):
            print("Best score is equal to average score, stopping at iteration " + str(i))
            stop_callback("Best score is equal to average score, stopping at iteration " + str(i))
            break
        # Met à jour la barre de progression de l'interface graphique
        progress_callback(i)
    print("Done!")
    return best_list, average_list


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
        if (i % 10 == 0):  # Affichage toutes les 10 itérations
            print("Itération " + str(i))
    # Affichage à la fin de l'exécution
    print("Done!")
    plt.show()

if __name__ == "__main__" :
    execute_main(
            nb_iterations = 150,
            mutation_rate = 0.05,
            population_size = 1000, 
            country = "Colombia", 
            nb_cities = 18,
            pause = 0.01)

#TODO : interface graphique, pourquoi pas : affichage de graphiques (en R ?) pour les statistiques sur les scores de chaque itération
#TODO : barre de progression dans l'interface graphique 
