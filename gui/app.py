import customtkinter as ctk
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from genetic_algorithm import GeneticAlgorithm as algoGen
from genetic_algorithm import main as main
from StartPage import StartPage
from MainPage import MainPage
from ResultsPage import ResultsPage
import time

####################################################
#!###### Création de la fenêtre principale #########
#!####  Gestion de l'affichage des fenêtres  #######
####################################################
ctk.set_appearance_mode("light")
#TODO : Configurer les couleurs en light et darkmode (faire un .json avec un thème custom : 
#TODO :                                              VOIR AVEC JEAN POUR LES COULEURS)
#       -> Proposer un bouton pour switch

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        #! Initialisation des paramètres par défaut
        self.mutation_rate = 0.05
        self.population_size = 500
        self.country = 'France'
        self.nb_routes = 1
        self.nb_iterations = 500
        self.nb_cities = 17

        self.title("Algo génétique")
        self.geometry("1400x1000")
        self.protocol("WM_DELETE_WINDOW", self.quit)
        self.configure(fg_color="white")

        with open('data\countries.txt', 'r') as file:
            self.countries = [line.strip() for line in file.readlines()]
        self.toStartWindow()


    def set_iterations(self, value):
        self.nb_iterations = round(value)

    def get_nb_iterations(self):
        return self.startPage.mainFrame.iterationsSlider.get()    

    def set_nbCities(self, value):
        self.nb_cities = round(value)

    def get_nb_cities(self):
        return self.startPage.mainFrame.nbCitiesSlider.get()

    def update_stats(self, best, average):
        self.mainPage.statsFrame.setStatsTexts(best, average)

    def toStartWindow(self):
        if hasattr(self, 'resultsPage'):
            self.resultsPage.destroy()
        self.startPage = StartPage(master=self, fg_color="white", to_main_window=self.toMainWindow, 
                                set_iterations= self.set_iterations, set_nbCities=self.set_nbCities, 
                                update_stats=self.update_stats, mutation_rate=self.mutation_rate, 
                                population_size=self.population_size, country=self.country, 
                                nb_routes=self.nb_routes, nb_iterations=self.nb_iterations, 
                                nb_cities=self.nb_cities)                       
        self.startPage.pack(fill="both", expand=True)
        self.startPage.mainFrame.iterationsSlider.set(self.nb_iterations)
        self.startPage.mainFrame.nbCitiesSlider.set(self.nb_cities)
        self.startPage.mainFrame.iterationsSliderLabel.configure(text="Nombre d'itérations : " + str(self.nb_iterations))
        self.startPage.mainFrame.nbCitiesSliderLabel.configure(text="Nombre de villes : " + str(self.nb_cities))
    
    def toMainWindow(self, nb_iterations):
        # Obtention des valeurs des paramètres
        mutation_rate = self.startPage.mainFrame.get_mutation_rate()
        population_size = self.startPage.mainFrame.get_population_size()
        country = self.startPage.mainFrame.get_country()
        nb_routes = self.startPage.mainFrame.get_nb_routes()
        nb_iterations = self.get_nb_iterations()
        nb_cities = self.get_nb_cities()
        # Stockage des nouvelles valeurs des paramètres
        self.mutation_rate = mutation_rate
        self.population_size = population_size
        self.country = country
        self.nb_routes = nb_routes
        # Destruction de l'ancienne fenêtre et création de la nouvelle
        self.startPage.destroy()
        self.mainPage = MainPage(master=self, fg_color="white", nb_iterations = nb_iterations)
        self.mainPage.pack(fill="both", expand=True)
        self.start_algorithm(mutation_rate, population_size, country, nb_routes)

    def toResultsWindow(self):
        self.mainPage.destroy()
        self.resultsPage = ResultsPage(master = self, fg_color="white")
        self.resultsPage.pack(fill="both", expand = True)

    def start_algorithm(self, mutation_rate, population_size, country, nb_routes):
        main.execute(
            nb_iterations= self.nb_iterations,
            canvas=self.mainPage.mapFrame.canvas, 
            fig=self.mainPage.mapFrame.fig, 
            gax=self.mainPage.mapFrame.gax, 
            mutation_rate = mutation_rate,
            population_size= population_size, 
            country = country,
            root=self,
            nb_cities=self.nb_cities,
            pause=0.02,
            progress_callback=self.mainPage.topMapFrame.setProgressIteration,
            stats_callback = self.mainPage.statsFrame.setStatsTexts,
            nb_routes = nb_routes,
            stop_callback = self.mainPage.topMapFrame.setStopMessage 
        )
        self.mainPage.parametersFrame.next_button()


app = App()
app.mainloop()