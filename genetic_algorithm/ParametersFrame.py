import GeneticAlgorithm as algoGen
import main as main
import customtkinter as ctk
class ParametersFrame(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.start_btn = ctk.CTkButton(master=self, text="Start", font=("Arial", 34), 
                                       command=self.start_algorithm)
        self.start_btn.place(relx=0.5, rely=0.5, anchor="center")

    def start_algorithm(self):
        main.execute(
            nb_iterations=100,
            canvas=self.master.mapFrame.canvas, 
            fig=self.master.mapFrame.fig, 
            gax=self.master.mapFrame.gax, 
            mutation_rate=0.04,
            population_size=100, 
            country=country, 
            root=self.master,
            nb_cities=15,
            pause=0.02,
            progress_callback=self.master.topMapFrame.setProgressIteration
        )