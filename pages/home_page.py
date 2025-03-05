import customtkinter as ctk
from pages.debate_page import DebatePage

class HomePage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        self.label = ctk.CTkLabel(self, text="Who would you like to debate against?", font=("Arial", 30))
        self.label.grid(row=0, column=0, pady=20, padx=20, sticky="n")
        
        self.entry = ctk.CTkEntry(self, placeholder_text="Enter opponent name")
        self.entry.grid(row=1, column=0, pady=300, padx=700, sticky="nsew")
        
        self.start_button = ctk.CTkButton(
            self, text="Start Debate", height=40,
            command=lambda: controller.show_frame(DebatePage, self.entry.get() or "AI Opponent")
        )
        self.start_button.grid(row=2, column=0, pady=20, padx=20, sticky="s")
        