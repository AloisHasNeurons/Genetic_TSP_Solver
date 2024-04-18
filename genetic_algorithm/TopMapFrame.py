import customtkinter as ctk
from customtkinter import CTkProgressBar

class TopMapFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.progress = ctk.CTkProgressBar(master=self, height=30)
        self.progress.place(relx=0.5, rely=0.5, anchor="center")
        self.progress.set(0)

    def setProgressIteration(i):
        self.progress.set(i/nb_iterations)
