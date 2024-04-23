import customtkinter as ctk
class ResultsPage(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        # Title
        self.titleFrame = ResultsTitleFrame(master=self,fg_color="black")
        self.titleFrame.grid(row=0, column=0, columnspan=5, sticky="nsew")

        # Graphs (placeholder for now)
        self.graphsFrame = GraphsFrame(master=self,fg_color="white")
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
        self.title = ctk.CTkLabel(master=self, text="Résultats", font=("Helvetica", 20))
        self.title.pack(anchor = "center")

class GraphsFrame(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.graphs = ctk.CTkLabel(master=self, text="Graphiques ici", font=("Helvetica", 20))
        self.graphs.pack()

class ButtonsFrame(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.restart_button = ctk.CTkButton(master=self, font=("Helvetica", 34),
                                            fg_color="white", text_color="black",
                                            border_width=2, border_color="black",
                                            hover_color="lightgreen", text="Recommencer", command=self.restart)
        self.restart_button.place(relx =0.4, rely = 0.5,anchor="center")
        self.quit_button = ctk.CTkButton(master=self, font=("Helvetica", 34),
                                         fg_color="white", text_color="black",
                                         border_width=2, border_color="black",
                                         hover_color="lightcoral", text="Quitter", command=self.quit)
        self.quit_button.place(relx =0.6, rely = 0.5,anchor="center")

    #? Méthodes associées aux boutons
    def restart(self):
        self.master.master.toStartWindow()

    def quit(self):
        self.master.quit()