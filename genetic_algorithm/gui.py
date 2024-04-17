import customtkinter as ctk
import main as main
import GeneticAlgorithm as algoGen
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import time

###########################################
# Initialisation des valeurs par défaut : #
###########################################
mutation_rate = 0.04
population_size = 100
country = "France"
nb_iterations = 100
###########################################
###########################################
###########################################


# Initialisation de la fenêtre
root = ctk.CTk()
root.title("Algo génétique")
root.geometry("1200x800")

# Initialisation des sections
mapFrame = ctk.CTkFrame(master = root, fg_color= "red")
statsFrame = ctk.CTkFrame(master= root, fg_color="green")
parametersFrame = ctk.CTkFrame(master= root, fg_color="blue")

mapFrame.grid(row = 0, column = 0, rowspan = 10, columnspan = 3, sticky="nsew")
statsFrame.grid(row = 0, column = 3, rowspan = 5, columnspan = 7, sticky="nsew")
parametersFrame.grid(row = 5, column = 3, rowspan = 5, columnspan = 7, sticky="nsew")


mapFrame.grid_rowconfigure(0, weight=1)
mapFrame.grid_columnconfigure(0, weight=1)

# Création des grilles de la fenêtre et de chaque section
for i in range(10) : 
    root.grid_rowconfigure(i, weight=1)
for i in range(10) : 
    root.grid_columnconfigure(i, weight=1)



for i in range(10) : 
    statsFrame.grid_rowconfigure(i, weight=0)
for i in range(10) : 
    statsFrame.grid_columnconfigure(i, weight=0)

for i in range(10) : 
    parametersFrame.grid_rowconfigure(i, weight=0)
for i in range(10) : 
    parametersFrame.grid_columnconfigure(i, weight=0)

# Figure
fig, gax = plt.subplots(figsize=(10,10))
canvas = FigureCanvasTkAgg(fig, master = mapFrame)
canvas.get_tk_widget().pack(side = "left", fill = "both", expand = True)


start_btn = ctk.CTkButton(master = parametersFrame, text="Start", font=("Arial", 34), 
                          command= lambda : main.execute(
                           nb_iterations = 100,
                           canvas = canvas, 
                           fig = fig, 
                           gax = gax, 
                           mutation_rate = 0.04,
                           population_size = 100, 
                           country = "France", 
                           root = root,
                           nb_cities = 15,
                           pause = 0.01))
start_btn.grid(row=7, column=1,columnspan = 2, rowspan = 2, sticky="nsew")


def on_closing():
    # Annuler tous les événements planifiés ici avec after_cancel
    # Exemple : root.after_cancel(id_de_mon_event_after)
    
    # Arrêter la boucle principale
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()