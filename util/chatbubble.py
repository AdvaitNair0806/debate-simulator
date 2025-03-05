import customtkinter as ctk
class ChatBubble(ctk.CTkFrame):
    def __init__(self, parent, text, align="left", isSystem=False):
        super().__init__(parent)
        bubble_color = "#DCF8C6" if align == "left" else "#ADD8E6"  # WhatsApp-like colors

        self.bubble = ctk.CTkFrame(self, fg_color=bubble_color, corner_radius=15)
        self.bubble.pack(padx=10, pady=5, anchor="w" if align == "left" else "e", fill="both")
        self.label = ctk.CTkLabel(self.bubble, text=text, wraplength=1500, fg_color="transparent", text_color="black")
        self.label.pack(padx=10, pady=5, anchor="w" if align == "left" else "e")

    def update_text(self, new_text):
        self.label.configure(text=new_text)