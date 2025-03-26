import customtkinter as ctk
from pages.home_page import HomePage
from pages.debate_page import DebatePage
from server.debate_manager import DebateManager

ctk.set_default_color_theme("themes/dark-blue.json")

class DebateSimulatorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Debate Simulator")
        self.geometry("1920x1080")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Create DebateManager inside the app
        self.manager = DebateManager()  # Now all pages can access this

        self.container = ctk.CTkFrame(self)
        self.container.grid(row=0, column=0, sticky="nsew")
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_rowconfigure(0, weight=1)

        self.frames = {}
        self.frames["HomePage"] = HomePage
        self.frames["DebatePage"] = DebatePage

        self.show_frame(HomePage)

    def show_frame(self, page, *args):
        frame = page(self.container, self, *args)  # Pass `self` (which has `manager`)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()

if __name__ == "__main__":
    app = DebateSimulatorApp()
    app.mainloop()
