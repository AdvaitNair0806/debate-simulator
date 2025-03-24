import customtkinter as ctk
from pages.debate_page import DebatePage

class HomePage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        self.configure(fg_color=["#1a1a1a", "#1a1a1a"])
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0) 
        self.grid_rowconfigure(1, weight=1) 
        
        self.header_frame = ctk.CTkFrame(
            self, 
            fg_color=["#2b2b2b", "#2b2b2b"],
            corner_radius=0,
            height=80
        )
        self.header_frame.grid(row=0, column=0, sticky="ew")
        self.header_frame.grid_columnconfigure(0, weight=1)

        self.header_label = ctk.CTkLabel(
            self.header_frame, 
            text="Debate Simulator", 
            font=("Helvetica", 32, "bold"),
            text_color=["#ffffff", "#ffffff"]
        )
        self.header_label.grid(row=0, column=0, pady=20, padx=20)

        self.content_frame = ctk.CTkFrame(
            self,
            fg_color=["#242424", "#242424"],
            corner_radius=15
        )
        self.content_frame.grid(row=1, column=0, pady=40, padx=40, sticky="nsew")
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure((0, 1, 2), weight=1)

        self.welcome_label = ctk.CTkLabel(
            self.content_frame, 
            text="Who would you like to debate against?",
            font=("Helvetica", 24),
            text_color=["#ffffff", "#ffffff"]
        )
        self.welcome_label.grid(row=0, column=0, pady=(40, 20), padx=20)

        self.entry = ctk.CTkEntry(
            self.content_frame,
            placeholder_text="Enter opponent name...",
            height=45,
            width=300,
            font=("Helvetica", 14),
            corner_radius=10,
            fg_color=["#333333", "#333333"],
            border_color=["#3a7a33", "#3a7a33"],
            border_width=2
        )
        self.entry.grid(row=1, column=0, pady=20, padx=20)
        
        self.start_button = ctk.CTkButton(
            self.content_frame,
            text="Start Debate ➤",
            width=200,
            height=50,
            corner_radius=10,
            font=("Helvetica", 16, "bold"),
            fg_color=["#3a7a33", "#3a7a33"],
            hover_color=["#2d5a27", "#2d5a27"],
            command=self.start_debate
        )
        self.start_button.grid(row=2, column=0, pady=(20, 40), padx=20)

        self.entry.bind("<Return>", lambda event: self.start_debate())
    
    def start_debate(self):
        opponent = self.entry.get() or "AI Opponent"
        self.controller.show_frame(DebatePage, opponent)