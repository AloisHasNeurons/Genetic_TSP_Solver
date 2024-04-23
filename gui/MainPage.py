import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
class MainPage(ctk.CTkFrame):
    def __init__(self, nb_iterations, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.topMapFrame = TopMapFrame(master=self, fg_color="gray2", nb_iterations=nb_iterations)
        self.topMapFrame.grid(row=0, column=0, columnspan=4, sticky="nsew")
        self.statsFrame = StatsFrame(master=self, fg_color="violet")
        self.statsFrame.grid(row=0, column=4, sticky="nsew")
        self.mapFrame = MapFrame(master=self, fg_color="gray94")
        self.mapFrame.grid(row=1, column=0, columnspan=5, sticky="nsew")

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        for i in range(5) :
            self.grid_columnconfigure(i, weight=1)

###################################################
#!########### Frames de MainPage : ################
###################################################

class TopMapFrame(ctk.CTkFrame):
    def __init__(self, master, nb_iterations, **kwargs):
        super().__init__(master, **kwargs)
        self.progress = ctk.CTkProgressBar(master=self, width = 500, height=20, corner_radius = 0, 
                                           border_width = 2, border_color = "grey",
                                           progress_color = "lime")
        self.progress.place(relx=0.5, rely=0.2, anchor="center")
        self.progress.set(0)
        self.nb_iterations = nb_iterations

        self.progressLabel = ctk.CTkLabel(master=self, text="Iteration 0/" + str(round(nb_iterations)), font=("Helvetica", 20), text_color = "LavenderBlush")
        self.progressLabel.place(relx=0.5, rely=0.05, anchor="center")

        self.stopLabel = ctk.CTkLabel(master=self, text="", font=("Helvetica", 20), text_color = "LavenderBlush")
        self.stopLabel.place(relx=0.5, rely=0.35, anchor="center")

    def setProgressIteration(self, i):
        self.progress.set(i/(self.nb_iterations-1))
        self.progressLabel.configure(text="Iteration " + str(i+1) + "/" + str(round(self.nb_iterations)))

    def setStopMessage(self, i):
           self.stopLabel.configure(text=str(i))

    def next_button(self):
        self.next_button = ctk.CTkButton(master=self, text="Next", font=("Helvetica", 34),
                                        fg_color="white", text_color="black", width= 200, height=100,
                                        border_width=2, border_color="black",
                                        hover_color="violet", anchor = 'center',
                                        command=self.master.master.toResultsWindow)
        
        self.next_button.place(relx = 0.43, rely = 0.5)

class MapFrame(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.fig, self.gax = plt.subplots(figsize=(10,10))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(fill=ctk.BOTH, expand=True)
        
class StatsFrame(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.statsTitle = ctk.CTkLabel(master = self, text = "Runtime statistics :", font = ("Helvetica", 28))
        self.bestRoute = ctk.CTkLabel(master = self, text = "Shortest distance = ", font= ("Helvetica", 20))
        self.averageRoute = ctk.CTkLabel(master = self, text = "Average distance = ", font= ("Helvetica", 20))
        self.statsTitle.place(relx=0.02, rely=0.05)
        self.bestRoute.place(relx=0.05, rely=0.4)
        self.averageRoute.place(relx=0.05, rely=0.6)

    def setStatsTexts(self, best, average) :
        self.bestRoute.configure(text = "Shortest distance = " + str(best) + " km")
        self.averageRoute.configure(text = "Average distance = " + str(average) + " km")
        

class ParametersFrame(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)


