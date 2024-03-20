from chemin import chemin
from city import city
from methodes_genetique import *
import numpy as np
import random
import matplotlib.pyplot as plt

#! Compteur du nombre de fois où Python m'a rendu fou :
#! 7

#TODO :
# Interface graphique :
### On pourra rentrer le nombre de villes dans l'interface
### La grille se calculerait en fonction du nombre de villes
# Affichage des chemins en temps réél lors du calcul
# Donner de vrais noms de villes existantes qu'on piocherait dans un tableau par exemple
#! On doit revenir à la ville de départ à la fin


#! Nommage : 
## Un individu (parent ou enfant) = un chemin solution, de taille nb_cities
## Une population = un ensemble de chemins solution
## Taille de la population = nombre de parents à évaluer en simultané

#################################################################################################
###########################  Initialisation  ####################################################
#################################################################################################
plt.ion




#################################################################################################
###########################  Affichages des graphiques  #############################################
#################################################################################################

#? Tracer le chemin des parents sur le graphique
def tracerChemin(tabParents):
    plt.cla()
    # Extraction des attributs des villes
    names = [city.name for city in cities]
    xs = [city.x for city in cities]
    ys = [city.y for city in cities]

    # Affichage des villes
    plt.scatter(xs, ys, c='red', marker='.')
    # Annotations
    for i, name in enumerate(names):
        plt.text(xs[i], ys[i], name)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Carte des villes générées aléatoirement')
    
    # Tracer les chemins entre chaque ville de chaque parent
    for i in range(len(tabParents)):
        colors = ['red','blue','green','purple','pink']
        #On va tracer le chemin
        cheminDraw = tabParents[i].cities
        for j in range((nb_cities)):
            plt.plot([cheminDraw[j].x, cheminDraw[j+1].x], [cheminDraw[j].y, cheminDraw[j+1].y], color = colors[i])
        
    #Mettre le score des chemins en légende
    # plt.legend([tabParents[i].score for i in range(len(tabParents))], 
    #            title="Scores des chemins (Plus est mieux)", 
    #            loc="lower left",)

    #? Garde le graphique ouvert lors de l'exécution du code
    plt.show(block = False)    
    plt.pause(0.5)



#################################################################################################
###########################  Affichage des parents  #############################################
#################################################################################################

#? Test de la génération des parents -> affichage console
def showParentScore(tabParents):
    for i in range(len(tabParents)):
        cheminParent = tabParents[i].cities
        print("\nParent " + str(i) + " Score :" + str(tabParents[i].score))
        # for j in cheminParent:
        #      print(j.toString())


#################################################################################################
###########################  Affichage des enfants  #############################################
#################################################################################################

# Affichage de tabEnfants pour vérifier le bon fonctionnement de genEnfants
def showEnfantScore(tabEnfants):
    for i in range(len(tabEnfants)):
        chemin_enfant = tabEnfants[i]
        print("\nEnfant " + str(i) + " Score :" + str(chemin_enfant.score))
        # for ville in chemin_enfant.cities:
        #     print(ville.toString())



#################################################################################################
############################  Itérations  Algo génétique ########################################
#################################################################################################
newGen = generateParents(nb_parents, cities)
tabParents = [0,0]
for i in range(10):
    print("\n###############")
    print("Itération " + str(i))
    print("###############")
    tabParents[0] = newGen[0]
    tabParents[0].cities = mutate(tabParents[0], 0.5)
    tabParents[1] = newGen[1]
    tabParents[1].cities = mutate(tabParents[1], 0.5)

    tabEnfants = genEnfants2(tabParents[0], tabParents[1])
    showEnfantScore(tabEnfants)
    newGen = select(tabEnfants, tabParents)

    tracerChemin(newGen)


