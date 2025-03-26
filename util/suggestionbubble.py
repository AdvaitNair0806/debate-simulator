import customtkinter as ctk

class CollapsibleSuggestionBubble(ctk.CTkFrame):
    def __init__(self, parent, text=""):
        super().__init__(parent, fg_color=["#2b2b2b", "#2b2b2b"], corner_radius=10)
        self.expanded = False

        # Toggle button
        self.toggle_button = ctk.CTkButton(
            self, 
            text="🔽 Show Suggestions", 
            width=200, 
            height=30,
            fg_color=["#444", "#444"],
            hover_color=["#666", "#666"],
            command=self.toggle
        )
        self.toggle_button.grid(row=0, column=0, sticky="ew", padx=10, pady=5)

        # Hidden text area (Initially not shown)
        self.text_label = ctk.CTkLabel(
            self, 
            text=text, 
            wraplength=1500, 
            justify="left",
            text_color=["#ffffff", "#ffffff"]
        )

    def toggle(self):
        if self.expanded:
            self.text_label.grid_forget()
            self.toggle_button.configure(text="🔽 Show Suggestions")
        else:
            self.text_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)
            self.toggle_button.configure(text="🔼 Hide Suggestions")
        self.expanded = not self.expanded

    def update_text(self, new_text):
        self.text_label.configure(text=new_text)