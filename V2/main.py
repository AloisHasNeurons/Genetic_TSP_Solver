import matplotlib.pyplot as plt
from matplotlib import image as mpimpg
import numpy as np
import random

################################################
# Binôme : Aloïs VINCENT et Jean REESE
# Implémentation d'un algorithme génétique pour résoudre le problème du voyageur de commerces
################################################

image = mpimpg.imread("V2/map.jpg")
plt.imshow(image)

#?                      x   y     Localisation
city_list = np.array([[290,180],  #Paris
                      [390,420],  #Marseille
                      [380,320],  #Lyon
                      [250,410],  #Toulouse
                      [450,410],  #Nice
                      [170,260],  #Nantes
                      [340,410],  #Montpellier
                      [460,200],  #Strasbourg
                      [200,360],  #Bordeaux
                      [310,100]]) #Lilles
nb_cities = len(city_list)
plt.scatter(city_list[:, 0], city_list[:, 1], color='red', marker='o', label='Villes')
plt.show()

#####################################
#!#### Génération des parents #######
#####################################
#? A partir de la liste de villes, créer 10 chemins "parents"
#? Ordre aléatoire, mais la première ville doit également être la dernière du chemin

def generateParents(nb_parents) :
    # Initialisation 
    indexes = list((range(1,nb_cities)))
    populationParent = [None] * (nb_parents)
    orderedList = [[None]] * (nb_cities+1)

    for i in range(nb_parents):
        # On change l'ordre de remplissage
        random.shuffle(indexes)

        # Pour remplir un parent aléatoire
        for j in range(1,nb_cities) :
            orderedList[j] = city_list[indexes[j-1]]
        orderedList[0] = city_list[0]
        orderedList[-1] = city_list[0]
        # On ajoute ce parent à la population
        populationParent[i] = orderedList

    # On renvoie un tableau de n parents néo-formés
    return populationParent
