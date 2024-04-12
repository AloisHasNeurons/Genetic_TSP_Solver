import customtkinter as ctk
# import main 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Initialisation de la fenêtre
root = ctk.CTk()
root.title("Algo génétique")
root.geometry("1800x1200")

# Initialisation des sections
mapFrame = ctk.CTkFrame(master = root, fg_color= "red")
statsFrame = ctk.CTkFrame(master= root, fg_color="green")
variablesFrame = ctk.CTkFrame(master= root, fg_color="blue")

mapFrame.grid(row = 0, column = 0, rowspan = 10, columnspan = 3, sticky="nsew")
statsFrame.grid(row = 0, column = 3, rowspan = 5, columnspan = 7, sticky="nsew")
variablesFrame.grid(row = 5, column = 3, rowspan = 5, columnspan = 7, sticky="nsew")

# Création des grilles de la fenêtre et de chaque section
for i in range(10) : 
    root.grid_rowconfigure(i, weight=1)
for i in range(10) : 
    root.grid_columnconfigure(i, weight=1)



for i in range(10) : 
    statsFrame.grid_rowconfigure(i, weight=1)
for i in range(10) : 
    statsFrame.grid_columnconfigure(i, weight=1)

for i in range(10) : 
    variablesFrame.grid_rowconfigure(i, weight=1)
for i in range(10) : 
    variablesFrame.grid_columnconfigure(i, weight=1)

# Figure
fig, gax = plt.subplots(figsize=(10,10))
canvas = FigureCanvasTkAgg(fig, master = mapFrame)
canvas.draw()
canvas.get_tk_widget().pack(side = "left", fill = "both", expand = True)



root.mainloop()