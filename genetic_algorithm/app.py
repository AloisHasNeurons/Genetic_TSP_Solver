import customtkinter as ctk
import GeneticAlgorithm as algoGen
import main as main
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time

####################################################
#!###### Création de la fenêtre principale #########
#!####  Gestion de l'affichage des fenêtres  #######
####################################################

#TODO : Configurer les couleurs en light et darkmode
#       -> Proposer un bouton pour switch

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Algo génétique")
        self.geometry("1400x1000")
        self.protocol("WM_DELETE_WINDOW", self.quit)
        self.configure(fg_color="white")
        self.toStartWindow()

        #! Paramètres de l'algo :
        self.nb_iterations = 100

    def set_iterations(self, value):
        self.nb_iterations = round(value)

    def update_stats(self, best, average):
        self.mainPage.statsFrame.setStatsTexts(best, average)

    def toStartWindow(self):
        self.startPage = StartPage(master=self, fg_color="red", to_main_window=self.toMainWindow, set_iterations= self.set_iterations,  update_stats=self.update_stats)
        self.startPage.pack(fill = "both", expand = True)
    
    def toMainWindow(self, nb_iterations):
        self.nb_iterations = nb_iterations
        self.startPage.destroy()
        self.mainPage = MainPage(master=self, fg_color="white", nb_iterations = nb_iterations)
        self.mainPage.pack(fill="both", expand=True)
        self.start_algorithm()

    def start_algorithm(self):
        country = "France"
        main.execute(
            nb_iterations= self.nb_iterations,
            canvas=self.mainPage.mapFrame.canvas, 
            fig=self.mainPage.mapFrame.fig, 
            gax=self.mainPage.mapFrame.gax, 
            mutation_rate=0.04,
            population_size=100, 
            country=country, 
            root=self,
            nb_cities=15,
            pause=0.02,
            progress_callback=self.mainPage.topMapFrame.setProgressIteration,
            stats_callback = self.mainPage.statsFrame.setStatsTexts
        )

####################################################
#!########### Création des 3 fenêtres ##############
####################################################

class StartPage(ctk.CTkFrame):
    def __init__(self, master=None, to_main_window=None, set_iterations=None, update_stats=None, **kwargs):
        super().__init__(master, **kwargs)

        for i in range(3) :
            self.grid_rowconfigure(i, weight=1)
        for i in range(5) :
            self.grid_columnconfigure(i, weight=1)
            
        self.titleFrame = TitleFrame(master=self, fg_color = "ghostwhite")
        self.mainFrame = MainFrame(master = self, fg_color = "lightgreen", set_iterations=set_iterations, update_stats=update_stats)
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
    def __init__(self, master, set_iterations=None, update_stats=None, **kwargs):
        self.set_iterations = set_iterations
        self.update_stats = update_stats
        super().__init__(master, **kwargs)
        self.iterationsSlider = ctk.CTkSlider(master = self, from_= 10, to= 500, number_of_steps = 100,
                                              command=self.nb_iterationsSlide)
        self.iterationsSlider.place(relx=0.5, rely=0.5, anchor="center")
        self.iterationsSlider.set(100)

        self.iterationsSliderLabel = ctk.CTkLabel(master = self, text = "Nombre d'itérations :", font= ("Helvetica", 20))
        self.iterationsSliderValue = ctk.CTkLabel(master = self, text = "100", font= ("Helvetica", 20))
        self.iterationsSliderLabel.place(relx=0.5, rely=0.4, anchor="center")
        self.iterationsSliderValue.place(relx=0.5, rely=0.6, anchor="center")

    def nb_iterationsSlide(self, value):
        self.iterationsSliderValue.configure(text=round(value))
        self.set_iterations(value)


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
        self.progress = ctk.CTkProgressBar(master=self,width = 500, height=20, corner_radius = 0, border_width = 2, border_color = "black", progress_color = "lime")
        self.progress.place(relx=0.5, rely=0.5, anchor="center")
        self.progress.set(0)
        self.nb_iterations = nb_iterations

    def setProgressIteration(self, i):
        self.progress.set(i/(self.nb_iterations-1))


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


###################################################
#!########### Frames de ResultsPage : #############
###################################################


app = App()
app.mainloop()