from City import City
from GeneticAlgorithm import GeneticAlgorithm

################################################
# Binôme : Aloïs VINCENT et Jean REESE
# Implémentation d'un algorithme génétique pour résoudre le problème du voyageur de commerces
################################################

#####################################
#!###### Création des villes ########
#####################################

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
algo.iterate(gen0)

#TODO : interface graphique, pourquoi pas : affichage de graphiques (en R ?) pour les statistiques sur les scores de chaque itération