import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ResultsPage(ctk.CTkFrame):
    def __init__(self, master=None, best_list = None, average_list = None, **kwargs):
        super().__init__(master, **kwargs)

        # Title
        self.titleFrame = ResultsTitleFrame(master=self,fg_color="gray2")
        self.titleFrame.grid(row=0, column=0, columnspan=5, sticky="nsew")

        # Graphs
        self.graphsFrame = GraphsFrame(master=self, best_list = best_list, average_list = average_list, fg_color="gray94")
        self.graphsFrame.grid(row=1, rowspan = 3, column=0, columnspan=5, sticky="nsew")

        # Buttons
        self.buttonsFrame = ButtonsFrame(master=self,fg_color="white")
        self.buttonsFrame.grid(row=4, column=0, columnspan=5, sticky="nsew")


        for i in range(5) :
            self.grid_columnconfigure(i, weight=1)
            self.grid_rowconfigure(i, weight=1)

###################################################
#!########### Frames de ResultsPage : #############
###################################################
class ResultsTitleFrame(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.title = ctk.CTkLabel(master=self, text="Results", font=("Helvetica", 38), text_color = "LavenderBlush")
        self.title.place(relx=0.5, rely=0.5, anchor="center")

class GraphsFrame(ctk.CTkFrame):
    def __init__(self, master=None, best_list=None, average_list=None, **kwargs):
        super().__init__(master, **kwargs)

        # Créer une nouvelle figure
        self.figure = plt.Figure(figsize=(6, 5), dpi=100)

        # Ajouter un sous-graphique à la figure
        self.ax = self.figure.add_subplot(111)

        # Créer une liste de nombres de 1 à len(best_list)
        # Parce qu'on compte les itérations à partir de 1 et non 0
        x_values = range(1, len(best_list) + 1)

        # Dessiner les données sur le sous-graphique
        self.ax.plot(x_values, best_list, label='Best Distance')
        self.ax.plot(x_values, average_list, label='Average Distance')

        # Ajouter des axes et un titre
        self.ax.set_xlabel('Iterations')
        self.ax.set_ylabel('Distance (km)')
        self.ax.set_title('Evolution of average and minimum distance over iterations')

        # Ajouter une légende
        self.ax.legend()

        # Créer un canvas Tkinter avec la figure
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.draw()

        # Ajouter le canvas à la fenêtre Tkinter
        self.canvas.get_tk_widget().pack(side=ctk.TOP, fill=ctk.BOTH, expand=True)

class ButtonsFrame(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.restart_button = ctk.CTkButton(master=self, font=("Helvetica", 34),
                                            fg_color="white", text_color="black",
                                            border_width=2, border_color="black",
                                            hover_color="lightgreen", text="Restart?", command=self.restart)
        self.restart_button.place(relx =0.4, rely = 0.5,anchor="center")
        self.quit_button = ctk.CTkButton(master=self, font=("Helvetica", 34),
                                         fg_color="white", text_color="black",
                                         border_width=2, border_color="black",
                                         hover_color="lightcoral", text="Quit", command=self.quit)
        self.quit_button.place(relx =0.6, rely = 0.5,anchor="center")

    #? Méthodes associées aux boutons
    def restart(self):
        self.master.master.toStartWindow()

    def quit(self):
        self.master.quit()