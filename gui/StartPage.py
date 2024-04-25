import customtkinter as ctk
from tkinter import StringVar
import tkinter.ttk as ttk
class StartPage(ctk.CTkFrame):
    def __init__(self, master=None, to_main_window=None, set_iterations=None, set_nbCities=None, 
                 update_stats=None, mutation_rate=0.005, population_size=700, country='France', 
                 nb_routes=1, nb_iterations = 1000, nb_cities = 25, **kwargs):
        super().__init__(master, **kwargs)

        for i in range(5) :
            self.grid_rowconfigure(i, weight=1)
        for i in range(5) :
            self.grid_columnconfigure(i, weight=1)
            
        self.titleFrame = TitleFrame(master=self, fg_color = "gray2")
        self.mainFrame = MainFrame(master = self, fg_color = "gray94", set_iterations=set_iterations, 
                                   set_nbCities=set_nbCities, update_stats=update_stats, 
                                   mutation_rate=mutation_rate, population_size=population_size, 
                                   country=country, nb_routes=nb_routes, nb_iterations=nb_iterations, 
                                   nb_cities=nb_cities) 
        self.bottomFrame = BottomFrame(master=self, fg_color="gray94", to_main_window=to_main_window)

        self.titleFrame.grid( row = 0, rowspan = 1, column = 0, columnspan = 5, sticky="nsew")
        self.mainFrame.grid(  row = 1, rowspan = 3, column = 0, columnspan = 5, sticky="nsew")
        self.bottomFrame.grid(row = 4, rowspan = 1, column = 0, columnspan = 5, sticky="nsew")


###################################################
#!########### Frames de StartPage : ###############
###################################################
class TitleFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.title = ctk.CTkLabel(master = self, text = "Parameters input", font= ("Helvetica", 34), text_color= "LavenderBlush")
        self.title.place(relx=0.5, rely=0.5, anchor="center")

class MainFrame(ctk.CTkFrame):
    def __init__(self, master, set_iterations=None, set_nbCities=None, update_stats=None, mutation_rate=0.005, 
                 population_size=700, country='France', nb_routes=1, nb_iterations = 1000, nb_cities = 25, **kwargs):
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
        self.iterationsSlider.place(relx=0.1, rely=0.3, anchor="center")
        self.iterationsSlider.set(nb_iterations)
        self.iterationsSliderLabel = ctk.CTkLabel(master = self, text = "No. of iterations : 500", font= ("Helvetica", 20))
        self.iterationsSliderLabel.place(relx=0.1, rely=0.2, anchor="center")

        #? Slider du nombre de villes
        self.nbCitiesSlider = ctk.CTkSlider(master = self, from_= 3, to= 50, number_of_steps = 47,
                                            command=self.nb_CitiesSlide)
        self.nbCitiesSlider.place(relx=0.1, rely=0.7, anchor="center")
        self.nbCitiesSlider.set(nb_cities)  
        self.nbCitiesSliderLabel = ctk.CTkLabel(master = self, text = "No. of cities : 17", font= ("Helvetica", 20))
        self.nbCitiesSliderLabel.place(relx=0.1, rely=0.6, anchor="center")
        

        #? Entrée du taux de mutation 
        self.mutationRateEntry = ctk.CTkEntry(master = self, placeholder_text = "0.05", font= ("Helvetica", 20))
        self.mutationRateEntry.place(relx=0.9, rely=0.7, anchor="center")
        self.mutationRateEntry.insert(0, str(mutation_rate))  # Initialisation avec la valeur de mutation_rate

        self.mutationRateEntryLabel = ctk.CTkLabel(master = self, text = "Mutation Rate :", font= ("Helvetica", 20)) 
        self.mutationRateEntryLabel.place(relx=0.9, rely=0.6, anchor="center")

        #? Entrée de population_size
        self.populationSizeEntry = ctk.CTkEntry(master = self, placeholder_text = "500", font= ("Helvetica", 20))
        self.populationSizeEntry.place(relx=0.9, rely=0.3, anchor="center")
        self.populationSizeEntry.insert(0, str(population_size))  # Initialisation avec la valeur de population_size

        self.populationSizeEntryLabel = ctk.CTkLabel(master = self, text = "Population Size :", font= ("Helvetica", 20)) 
        self.populationSizeEntryLabel.place(relx=0.9, rely=0.2, anchor="center")


        #? ComboBox de countries
        self.countryVar = StringVar()
        self.countryVar.set(master.master.countries[29])  # default value = 'France'
        self.countryVar.set(country)  # Initialisation avec la valeur de country

        # Utilisation de ttk pour avoir une liste scrollable
        self.countryCombobox = ttk.Combobox(master=self, textvariable=self.countryVar, values=master.master.countries, state="readonly", font= ("Helvetica", 20))
        self.countryCombobox.place(relx=0.5, rely=0.25, anchor="center")
        
        #? Combobox du nombre de routes
        self.nbRoutesVar = StringVar()
        self.nbRoutesVar.set("1")  # default value = 1
        self.nbRoutesVar.set(str(nb_routes))  # Initialisation avec la valeur de nb_routes

        self.nbRoutesComboboxLabel = ctk.CTkLabel(master = self, text = "No. of routes drawn :", font= ("Helvetica", 20)) 
        self.nbRoutesComboboxLabel.place(relx=0.5, rely=0.6, anchor="center")
        self.nbRoutesCombobox = ttk.Combobox(master=self, textvariable=self.nbRoutesVar, values=[str(i) for i in range(1, 6)], 
                                                  state="readonly", font= ("Helvetica", 20))
        self.nbRoutesCombobox.place(relx=0.5, rely=0.7, anchor="center")

    #? Méthodes associées aux sliders 
    def nb_iterationsSlide(self, value):
        self.iterationsSliderLabel.configure(text="No. of iterations : " + str(round(value)))
        self.set_iterations(value)

    def nb_CitiesSlide(self, value):
        self.nbCitiesSliderLabel.configure(text="No. of cities : " + str(round(value)))
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
            return 0.005  # default value

    def get_population_size(self):
       try:
           population_size = int(self.populationSizeEntry.get())
           if 2 <= population_size <= 2147483647:  # max value of an int
               return population_size
           else:
               raise ValueError
       except ValueError:
           return 700  # default value

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
                                       fg_color="white", text_color="black", width= 200, height=100,
                                       border_width=2, border_color="black",
                                       hover_color="deepskyblue",
                                       command=lambda: to_main_window(self.master.master.nb_iterations))
        self.start_btn.place(relx=0.5, rely=0.5, anchor="center")