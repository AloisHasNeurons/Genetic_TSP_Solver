from chemin import chemin
from city import city
from methodes_genetique import *
import numpy as np
import random
import matplotlib.pyplot as plt

#! Compteur du nombre de fois où Python m'a rendu fou :
#! 6

#TODO :
# Interface graphique :
### On pourra rentrer le nombre de villes dans l'interface
### La grille se calculerait en fonction du nombre de villes
# Affichage des chemins en temps réél lors du calcul
# Donner de vrais noms de villes existantes qu'on piocherait dans un tableau par exemple


#! Nommage : 
## Un individu (parent ou enfant) = un chemin solution, de taille nb_cities
## Une population = un ensemble de chemins solution
## Taille de la population = nombre de parents à évaluer en simultané

#################################################################################################
###########################  Initialisation  ####################################################
#################################################################################################




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
plt.ion
plt.scatter(xs, ys, c='red', marker='.')
# Annotations
for i, name in enumerate(names):
    plt.text(xs[i], ys[i], name)
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Carte des villes générées aléatoirement')
#? Garde le graphique ouvert lors de l'exécution du code
plt.show(block = False)



#################################################################################################
###########################  Affichage des parents  #############################################
#################################################################################################

#? Test de la génération des parents -> affichage console
tabParents = generateParents(nb_parents, cities)

def showParentScore(tabParents):
    for i in range(len(tabParents)):
        cheminParent = tabParents[i].cities
        print("\nParent " + str(i) + " Score :" + str(tabParents[i].score))
        # for j in cheminParent:
        #     print(j.toString())

showParentScore(tabParents) # Affichage console

#? Tracer le chemin des parents sur le graphique
#TODO : transformer en fonction
# Pour chaque ligne du tableau de parents
def tracerChemin(tabParents):
    for i in range(len(tabParents)):
        colors = ['red','blue','green','purple','pink']
        #On va tracer le chemin
        cheminDraw = tabParents[i].cities
        for j in range((nb_cities-1)):
            plt.plot([cheminDraw[j].x, cheminDraw[j+1].x], [cheminDraw[j].y, cheminDraw[j+1].y], color = colors[i])
 
tracerChemin(tabParents)

plt.ioff()
plt.show()
plt.pause(0)



#################################################################################################
###########################  Affichage des enfants  #############################################
#################################################################################################

tabEnfants = genEnfants(tabParents[0], tabParents[1])

# Affichage de tabEnfants pour vérifier le bon fonctionnement de genEnfants
def showEnfantScore(tabEnfants):
    for i in range(len(tabEnfants)):
        chemin_enfant = tabEnfants[i]
        print("\nEnfant " + str(i) + " Score :" + str(chemin_enfant.score))
        # for ville in chemin_enfant.cities:
        #     print(ville.toString())

showEnfantScore(tabEnfants) # Affichage console



newGen = select(tabEnfants, tabParents)

print(newGen)