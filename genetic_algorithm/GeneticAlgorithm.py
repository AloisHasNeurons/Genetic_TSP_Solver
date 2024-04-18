from Population import Population
from Route import Route
import random
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
from matplotlib import image as mpimpg
import os
class GeneticAlgorithm:
    ######################################
    #!########## Constructeur ############
    ######################################       
    # Initialisation des paramètres de l'algo
    def __init__(self, mutation_rate, population_size, city_list, country, data_city):
        self.mutation_rate = mutation_rate
        self.population_size = population_size
        self.city_list = city_list
        self.nb_cities = len(city_list)
        self.country = country
        self.data_city = data_city
        self.gdf = gpd.GeoDataFrame(data_city, geometry="Coordinates")
        self.pop = self.init_population()
        self.previous_best = None
        self.capital = city_list[0]

        # This should be the path to the downloaded countries shapefile.
        if os.name == "nt" : # Windows
            shapefile_path = "data\\ne_10m_admin_0_map_units\\ne_10m_admin_0_map_units.shp"
        else : # Unix
            shapefile_path = "data/ne_10m_admin_0_map_units/ne_10m_admin_0_map_units.shp"
        # Load the shapefile
        self.countries_gdf = gpd.read_file(shapefile_path)

        # Extraction des attributs des villes
        self.names = [city.name for city in city_list]
        self.longitude = [city.longitude for city in city_list]
        self.latitude = [city.latitude for city in city_list]

    #####################################
    #!###### Traçage des chemins ########
    #####################################
    def drawBestRoutes(self, population, nb_routes, gax):
        # On efface les routes précédentes        
        gax.cla()

        data_city = self.data_city
        countries_gdf = self.countries_gdf

        # Sélection des données correspondantes au pays
        country_subset = countries_gdf[countries_gdf['NAME'] == self.country]

        # Plot the country
        country_subset.plot(ax=gax, edgecolor='black',color='white')
        # Plot the cities
        self.gdf.plot(ax=gax, color='red', alpha = 0.5, aspect = None)


        gax.set_xlabel('longitude')
        gax.set_ylabel('latitude')

        # Kill the spines
        gax.spines['top'].set_visible(False)
        gax.spines['right'].set_visible(False)

        # Label the cities
        for longitude, latitude, label in zip(self.longitude, self.latitude, self.names):
            gax.annotate(label, xy=(longitude,latitude), xytext=(4,4), textcoords='offset points')
        
        colors = ['red','purple','green','blue','pink']

        # Initialisation du nombre de routes à afficher 
        # On ne peut pas sélectionner plus de routes qu'il n'y en a dans la population
        nb_routes = min(nb_routes, len(population.routes))
        # 5 est notre nombre de routes maximal à afficher
        nb_routes = min(nb_routes, 5)

        # On trace les chemins
        for i in range(nb_routes) : 
            villes = population.routes[i].cities
            for j in range(len(villes) - 1):
                plt.plot([villes[j].longitude, villes[j+1].longitude], [villes[j].latitude, villes[j+1].latitude], color = colors[i])

        #? Garde le graphique ouvert lors de l'exécution du code
        # self.fig.canvas.draw()
        # plt.pause(0.05) #Nombre de secondes d'affichage
        return gax
    ##############################################################
    #!########## Génération d'une population initiale ############
    ##############################################################
    # Renvoie une population 
    def init_population(self):
        #? Ordre aléatoire, mais la première ville doit également être la dernière du chemin
        # Initialisation 
        indexes = list((range(1,self.nb_cities)))
        population = [None] * (self.population_size)
        city_list = self.city_list

        for i in range(self.population_size):
            orderedList = [None] * (self.nb_cities+1)
            # On change l'ordre de remplissage
            random.shuffle(indexes)
            # Pour remplir un parent aléatoire
            for j in range(1,self.nb_cities) :
                orderedList[j] = city_list[indexes[j-1]]
            # La première et la dernière ville sont fixées
            orderedList[0] = city_list[0]
            orderedList[-1] = city_list[0]
            newRoute = Route(i, orderedList)
            # On ajoute ce parent à la population
            population[i] = newRoute
        # On renvoie un tableau de n parents néo-formés
        return Population(city_list = city_list, routes = population)

    ###################################
    #!########## Crossover ############
    ###################################
    # Prend 2 parents, et renvoie deux Route enfants, qui correspondent aux parents avec des segments échangés
    def crossOverDeLaMortQuiTue(self, parent1, parent2):
        nb_cities = self.nb_cities
        start, end = sorted(random.sample(range(1, nb_cities), 2))
        p1, p2 = parent1.cities, parent2.cities # p = parent

        # On définit les segments à échanger :
        l1, l2 = p1[start:end+1], p2[start:end+1] # l = liste (je sais pas trop pourquoi mais c'était plus intuitif)
        # On fait des listes contenants les valeurs propres à un seul segment
        # Pour chaque élément de l1, qui n'est pas dans l2, on le met dans u1, et vice versa pour u2
        u1, u2 = [e for e in l1 if e not in l2], [e for e in l2 if e not in l1] # u = unique

        # On initialise les enfants, vides
        c1, c2 = [None] * (nb_cities+1), [None] * (nb_cities+1) # c = child
        # On copie les segments dans les enfants :
        c1[start:end+1] = l2 
        c2[start:end+1] = l1

        # On définit la première et la dernière ville
        for c in [c1, c2]:
             c[0] = c[-1] = self.city_list[0]

        # On remplit le reste des villes, sans toucher à la première et dernière ville
        def fill(c, p, u) :
            idx = 1
            for e in p: # Pour chaque élément du parent 
                if e not in u and e not in c: # Si il n'est pas dans la séquence unique à échanger, et qu'il n'est pas déjà ajouté
                    while c[idx] is not None and idx < nb_cities : # On parcourt l'enfant pour trouver un None 
                        idx += 1
                    c[idx] = e # On ajoute l'élément 
        fill(c1, p1, u2)
        fill(c2, p2, u1)
        
        if None in c1 or None in c2 :
        # Remplir les None restants dans c1 et c2
            for c in [c1, c2]:
                for i in range(len(c)):
                    if c[i] is None:
                        # Trouver un élément qui n'est pas encore dans c
                        for e in self.city_list:
                            if e not in c:
                                c[i] = e
                                break
        return Route("Child 1", c1), Route("Child 2", c2)

    ###############################################
    #!########## Fonctions de mutation ############
    ###############################################
    def mutate(self, population):
        for i in range(len(population.routes)): 
            for j in range(1, self.nb_cities - 1) :  
                if random.random() < self.mutation_rate:
                    x = random.randint(0, 2)
                    if x == 0 :
                        population.routes[j] = self.fullReverse(population=population, position = j)
                    elif x == 1 :
                        population.routes[j] = self.partReverse(population=population, position = j)
                    elif x == 2 :
                        population.routes[j] = self.moveTwo(population=population, position=j)
                    #TODO : Rajouter d'autres types de mutations 
        return population

    # Mutation qui inverse l'ordre de toutes les villes
    def fullReverse(self, population, position):
        cities = population.routes[position].cities
        # Slicing pour obtenir la liste inversée
        return Route(name = population.routes[position].name, cities=cities[::-1])

    # Mutation qui inverse l'ordre de deux villes adjacentes
    def partReverse(self, population, position):
        cities = population.routes[position].cities
        # Définition de la position de la mutation
        x = random.randint(2, self.nb_cities)
        #Vérification supplémentaire qu'on ne bouge pas la ville de départ
        while cities[x].name == self.capital.name or cities[x-1].name == self.capital.name :
            x = random.randint(2, self.nb_cities)  
        # Déballage de tuple pour échanger les positions  
        cities[x], cities[x - 1] = cities[x - 1], cities[x]
        return Route(name=population.routes[position].name, cities=cities)

    # Mutation qui interchange les positions de deux villes
    def moveTwo(self, population, position) :
        cities = population.routes[position].cities
        nb_cities = len(cities) - 1
        # Définition des positions à échanger mutation
        pos1, pos2 = random.randint(1, nb_cities), random.randint(1, nb_cities)
        # Vérification supplémentaire qu'on ne bouge pas la ville de départ, et que les positions 1 et 2 sont !=
        while cities[pos1].name == self.capital.name :
            pos1 = random.randint(1, nb_cities) 
        while pos1 == pos2 or cities[pos2].name == self.capital.name :
            pos2 = random.randint(1, nb_cities)
        # Déballage de tuple pour échanger les positions  
        cities[pos1], cities[pos2] = cities[pos2], cities[pos1]
        return Route(name=population.routes[position].name, cities=cities)

    ####################################
    #!########## Itérations ############
    ####################################
    # Produit une itération de l'algo
    def run(self) :
        previous_pop = self.pop
        self.previous_best = previous_pop.selectFittest(1)
        pop_size = self.population_size
        # On sélectionne les 50% meilleures Routes de la population précédente
        newPopRoutes = previous_pop.selectFittest(int(pop_size/2)).routes
        # On choisit des positions aléatoires, correspondant aux parents, qu'on met dans deux listes
        x, y = random.sample(range(pop_size), int(pop_size/2)), random.sample(range(pop_size), int(pop_size/2))
        # On fait des cross-overs
        for j in range(int(pop_size/2)):
            e1, e2 = self.crossOverDeLaMortQuiTue(previous_pop.routes[x[j]], previous_pop.routes[y[j]])
            newPopRoutes.append(e1)
            newPopRoutes.append(e2)
        # On fait des mutations sur le résultat de nos cross-overs
        newPop = Population(newPopRoutes, city_list=self.city_list)
        newPop = self.mutate(newPop)
        # On sélectionne les meilleurs individus pour constituer notre nouvelle population
        pop = newPop.selectFittest(pop_size)
        self.pop = pop
