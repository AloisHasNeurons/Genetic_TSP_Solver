import customtkinter as ctk
import GeneticAlgorithm as algoGen
import main as main
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import StringVar
import tkinter.ttk as ttk
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

####################################################
#!########### Création des 3 fenêtres ##############
####################################################

class StartPage(ctk.CTkFrame):
    def __init__(self, master=None, to_main_window=None, set_iterations=None, set_nbCities=None, 
                 update_stats=None, mutation_rate=0.05, population_size=500, country='France', 
                 nb_routes=1, nb_iterations = 500, nb_cities = 17, **kwargs):
        super().__init__(master, **kwargs)

        for i in range(3) :
            self.grid_rowconfigure(i, weight=1)
        for i in range(5) :
            self.grid_columnconfigure(i, weight=1)
            
        self.titleFrame = TitleFrame(master=self, fg_color = "ghostwhite")
        self.mainFrame = MainFrame(master = self, fg_color = "lightgreen", set_iterations=set_iterations, 
                                   set_nbCities=set_nbCities, update_stats=update_stats, 
                                   mutation_rate=mutation_rate, population_size=population_size, 
                                   country=country, nb_routes=nb_routes, nb_iterations=nb_iterations, 
                                   nb_cities=nb_cities) 
        self.bottomFrame = BottomFrame(master=self, fg_color="lightblue", to_main_window=to_main_window)

        self.titleFrame.grid( row = 0, rowspan = 1, column = 0, columnspan = 5, sticky="nsew")
        self.mainFrame.grid(  row = 1, rowspan = 1, column = 0, columnspan = 5, sticky="nsew")
        self.bottomFrame.grid(row = 2, rowspan = 1, column = 0, columnspan = 5, sticky="nsew")

class MainPage(ctk.CTkFrame):
    def __init__(self, nb_iterations, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.topMapFrame = TopMapFrame(master=self, fg_color="red", nb_iterations=nb_iterations)
        self.topMapFrame.grid(row=0, column=0, columnspan=3, sticky="nsew")
        self.mapFrame = MapFrame(master=self, fg_color="purple")
        self.mapFrame.grid(row=1, column=0)
        self.statsFrame = StatsFrame(master=self, fg_color="green")
        self.statsFrame.grid(row=0, column=3, columnspan=3, sticky="nsew")
        self.parametersFrame = ParametersFrame(master=self, fg_color="blue")
        self.parametersFrame.grid(row=1, column=3, columnspan=3, sticky="nsew")

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        for i in range(5) :
            self.grid_columnconfigure(i, weight=1)



class ResultsPage(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        # Title
        self.titleFrame = ResultsTitleFrame(master=self,fg_color="red")
        self.titleFrame.grid(row=0, column=0, columnspan=5, sticky="nsew")

        # Graphs (placeholder for now)
        self.graphsFrame = GraphsFrame(master=self,fg_color="lightblue")
        self.graphsFrame.grid(row=1, rowspan = 3, column=0, columnspan=5, sticky="nsew")

        # Buttons
        self.buttonsFrame = ButtonsFrame(master=self,fg_color="lightgreen")
        self.buttonsFrame.grid(row=4, column=0, columnspan=5, sticky="nsew")


        for i in range(5) :
            self.grid_columnconfigure(i, weight=1)
            self.grid_rowconfigure(i, weight=1)


###################################################
#!###########  Création des Frames  ###############
###################################################
#!########### Frames de StartPage : ###############
###################################################
class TitleFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.title = ctk.CTkLabel(master = self, text = "Entrée des paramètres", font= ("Helvetica", 34))
        self.title.place(relx=0.5, rely=0.5, anchor="center")

class MainFrame(ctk.CTkFrame):
    def __init__(self, master, set_iterations=None, set_nbCities=None, update_stats=None, mutation_rate=0.05, 
                 population_size=500, country='France', nb_routes=1, nb_iterations = 500, nb_cities = 17, **kwargs):
        self.set_iterations = set_iterations
        self.set_nbCities = set_nbCities
        self.update_stats = update_stats
        self.mutation_rate = mutation_rate
        self.population_size = population_size
        self.country = country
        self.nb_routes = nb_routes
        self.nb_iterations = nb_iterations
        self.nb_cities = nb_cities
        super().__init__(master, **kwargs)

        #? Slider du nombre d'itérations
        self.iterationsSlider = ctk.CTkSlider(master = self, from_= 50, to= 5000, number_of_steps = 99,
                                              command=self.nb_iterationsSlide)
        self.iterationsSlider.place(relx=0.1, rely=0.2, anchor="center")
        self.iterationsSlider.set(nb_iterations)
        self.iterationsSliderLabel = ctk.CTkLabel(master = self, text = "Nombre d'itérations : 500", font= ("Helvetica", 20))
        self.iterationsSliderLabel.place(relx=0.1, rely=0.1, anchor="center")

        #? Slider du nombre de villes
        self.nbCitiesSlider = ctk.CTkSlider(master = self, from_= 3, to= 50, number_of_steps = 47,
                                            command=self.nb_CitiesSlide)
        self.nbCitiesSlider.place(relx=0.1, rely=0.5, anchor="center")
        self.nbCitiesSlider.set(nb_cities)  
        self.nbCitiesSliderLabel = ctk.CTkLabel(master = self, text = "Nombre de villes : 17", font= ("Helvetica", 20))
        self.nbCitiesSliderLabel.place(relx=0.1, rely=0.4, anchor="center")
        

        #? Entrée du taux de mutation 
        self.mutationRateEntry = ctk.CTkEntry(master = self, placeholder_text = "0.05", font= ("Helvetica", 20))
        self.mutationRateEntry.place(relx=0.1, rely=0.8, anchor="center")
        self.mutationRateEntry.insert(0, str(mutation_rate))  # Initialisation avec la valeur de mutation_rate

        self.mutationRateEntryLabel = ctk.CTkLabel(master = self, text = "Mutation Rate :", font= ("Helvetica", 20)) 
        self.mutationRateEntryLabel.place(relx=0.1, rely=0.7, anchor="center")

        #? Entrée de population_size
        self.populationSizeEntry = ctk.CTkEntry(master = self, placeholder_text = "500", font= ("Helvetica", 20))
        self.populationSizeEntry.place(relx=0.5, rely=0.8, anchor="center")
        self.populationSizeEntry.insert(0, str(population_size))  # Initialisation avec la valeur de population_size

        self.populationSizeEntryLabel = ctk.CTkLabel(master = self, text = "Population Size :", font= ("Helvetica", 20)) 
        self.populationSizeEntryLabel.place(relx=0.5, rely=0.7, anchor="center")


        #? ComboBox de countries
        self.countryVar = StringVar()
        self.countryVar.set(master.master.countries[29])  # default value = 'France'
        self.countryVar.set(country)  # Initialisation avec la valeur de country

        # Utilisation de ttk pour avoir une liste scrollable
        self.countryCombobox = ttk.Combobox(master=self, textvariable=self.countryVar, values=master.master.countries, state="readonly", font= ("Helvetica", 20))
        self.countryCombobox.place(relx=0.5, rely=0.2, anchor="center")
        
        #? Combobox du nombre de routes
        self.nbRoutesVar = StringVar()
        self.nbRoutesVar.set("1")  # default value = 1
        self.nbRoutesVar.set(str(nb_routes))  # Initialisation avec la valeur de nb_routes

        self.nbRoutesComboboxLabel = ctk.CTkLabel(master = self, text = "Number of routes drawn :", font= ("Helvetica", 20)) 
        self.nbRoutesComboboxLabel.place(relx=0.5, rely=0.3, anchor="center")
        self.nbRoutesCombobox = ctk.CTkOptionMenu(master=self, variable=self.nbRoutesVar, values=[str(i) for i in range(1, 6)], state="readonly", font= ("Helvetica", 20))
        self.nbRoutesCombobox.place(relx=0.5, rely=0.4, anchor="center")

    #? Méthodes associées aux sliders 
    def nb_iterationsSlide(self, value):
        self.iterationsSliderLabel.configure(text="Nombre d'itérations : " + str(round(value)))
        self.set_iterations(value)

    def nb_CitiesSlide(self, value):
        self.nbCitiesSliderLabel.configure(text="Nombre de villes : " + str(round(value)))
        self.set_nbCities(value)

    #? Méthodes associées aux entries
    def get_mutation_rate(self):
        try:
            mutation_rate = float(self.mutationRateEntry.get())
            if 0 <= mutation_rate <= 1:
                return mutation_rate
            else:
                raise ValueError
        except ValueError:
            return 0.05  # default value

    def get_population_size(self):
       try:
           population_size = int(self.populationSizeEntry.get())
           if 2 <= population_size <= 2147483647:  # max value of an int
               return population_size
           else:
               raise ValueError
       except ValueError:
           return 500  # default value

    #? Méthodes associées aux Combobox
    def get_country(self):
        return self.countryVar.get()
    def get_nb_routes(self):
        return int(self.nbRoutesVar.get())

#* Paramètres à intégrer 
#pause



class BottomFrame(ctk.CTkFrame):
    def __init__(self, master, to_main_window=None, **kwargs):
        super().__init__(master, **kwargs)
        self.start_btn = ctk.CTkButton(master=self, text="Run!", font=("Helvetica", 34),
                                       fg_color="white", text_color="black",
                                       border_width=2, border_color="black",
                                       hover_color="lightgrey",
                                       command=lambda: to_main_window(self.master.master.nb_iterations))
        self.start_btn.place(relx=0.5, rely=0.5, anchor="center")
###################################################
#!########### Frames de MainPage : ################
###################################################

class TopMapFrame(ctk.CTkFrame):
    def __init__(self, master, nb_iterations, **kwargs):
        super().__init__(master, **kwargs)
        self.progress = ctk.CTkProgressBar(master=self, width = 500, height=20, corner_radius = 0, 
                                           border_width = 2, border_color = "black",
                                           progress_color = "lime")
        self.progress.place(relx=0.5, rely=0.5, anchor="center")
        self.progress.set(0)
        self.nb_iterations = nb_iterations

        self.progressLabel = ctk.CTkLabel(master=self, text="Itération 0/" + str(round(nb_iterations)), font=("Helvetica", 20))
        self.progressLabel.place(relx=0.5, rely=0.35, anchor="center")

        self.stopLabel = ctk.CTkLabel(master=self, text="", font=("Helvetica", 20))
        self.stopLabel.place(relx=0.5, rely=0.65, anchor="center")

    def setProgressIteration(self, i):
        self.progress.set(i/(self.nb_iterations-1))
        self.progressLabel.configure(text="Itération " + str(i+1) + "/" + str(round(self.nb_iterations)))

    def setStopMessage(self, i):
           self.stopLabel.configure(text=str(i))

class MapFrame(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.fig, self.gax = plt.subplots(figsize=(10,10))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

class StatsFrame(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.statsTitle = ctk.CTkLabel(master = self, text = "Statistiques de l'exécution :", font = ("Helvetica", 28))
        self.bestRoute = ctk.CTkLabel(master = self, text = "Plus petite distance = ", font= ("Helvetica", 20))
        self.averageRoute = ctk.CTkLabel(master = self, text = "Distance moyenne = ", font= ("Helvetica", 20))
        self.statsTitle.place(relx=0.02, rely=0.05)
        self.bestRoute.place(relx=0.05, rely=0.4)
        self.averageRoute.place(relx=0.05, rely=0.6)

    def setStatsTexts(self, best, average) :
        self.bestRoute.configure(text = "Plus petite distance = " + str(best) + " km")
        self.averageRoute.configure(text = "Distance moyenne  = " + str(average) + " km")
        

class ParametersFrame(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)


    def next_button(self):
        self.next_button = ctk.CTkButton(master=self, text="Next", command=self.master.master.toResultsWindow)
        self.next_button.pack()


###################################################
#!########### Frames de ResultsPage : #############
###################################################
class ResultsTitleFrame(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.title = ctk.CTkLabel(master=self, text="Résultats", font=("Helvetica", 20))
        self.title.pack()

class GraphsFrame(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.graphs = ctk.CTkLabel(master=self, text="Graphiques ici", font=("Helvetica", 20))
        self.graphs.pack()

class ButtonsFrame(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.open_map_button = ctk.CTkButton(master=self, text="Ouvrir la carte", command=self.open_map)
        self.open_map_button.pack(side="left")
        self.restart_button = ctk.CTkButton(master=self, text="Recommencer", command=self.restart)
        self.restart_button.pack(side="left")
        self.quit_button = ctk.CTkButton(master=self, text="Quitter", command=self.quit)
        self.quit_button.pack(side="left")

    #? Méthodes associées aux boutons
    def open_map(self):
        # Code to open the map
        pass

    def restart(self):
        self.master.master.toStartWindow()

    def quit(self):
        self.master.quit()

app = App()
app.mainloop()