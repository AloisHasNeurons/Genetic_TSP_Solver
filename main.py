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
plt.scatter(xs, ys, c='red', marker='.')
# Annotations
for i, name in enumerate(names):
    plt.text(xs[i], ys[i], name)
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Carte des villes générées aléatoirement')
plt.show()


