import customtkinter as ctk
import asyncio
import threading
import util.globals as globals
from util.chatbubble import ChatBubble
from util.suggestionbubble import CollapsibleSuggestionBubble
import time

class DebatePage(ctk.CTkFrame):
    def __init__(self, parent, controller, debate_opponent="AI Opponent", debate_stance="for"):
        super().__init__(parent)
        self.controller = controller
        self.debate_opponent = debate_opponent
        self.debate_stance = debate_stance
        self.debate_id = self.controller.manager.start_debate(debate_opponent, debate_stance)
        self.user_score = 0
        self.opponent_score = 0
        
        # Configure main frame
        self.configure(fg_color=["#1a1a1a", "#1a1a1a"])
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)  # Header
        self.grid_rowconfigure(1, weight=1)  # Chat area
        self.grid_rowconfigure(2, weight=0)  # Input area
        
        # Create header frame
        self.header_frame = ctk.CTkFrame(
            self, 
            fg_color=["#2b2b2b", "#2b2b2b"],
            corner_radius=0,
            height=80
        )
        self.header_frame.grid(row=0, column=0, sticky="ew")
        self.header_frame.grid_columnconfigure(1, weight=1)
        
        # Title with better styling
        self.label = ctk.CTkLabel(
            self.header_frame, 
            text=f"Debate Room - {self.debate_opponent}", 
            font=("Helvetica", 32, "bold"),
            text_color=["#ffffff", "#ffffff"]
        )
        self.label.grid(row=0, column=1, pady=20, padx=20, sticky="w")

        # User Score
        self.user_score_label = ctk.CTkLabel(
            self.header_frame, 
            text=f"Your Score: {self.user_score}", 
            font=("Helvetica", 14),
            text_color=["#ffffff", "#ffffff"]
        )
        self.user_score_label.grid(row=0, column=2, pady=20, padx=20, sticky="w")


        # Opponent Score
        self.opponent_score_label = ctk.CTkLabel(
            self.header_frame, 
            text=f"Opponent's Score: {self.opponent_score}", 
            font=("Helvetica", 14),
            text_color=["#ffffff", "#ffffff"]
        )
        self.opponent_score_label.grid(row=0, column=3, pady=20, padx=20, sticky="w")
        
        # Home button with styling
        self.back_button = ctk.CTkButton(
            self.header_frame,
            text="🏠 Home",
            width=120,
            height=40,
            corner_radius=10,
            font=("Helvetica", 14, "bold"),
            fg_color=["#3a7a33", "#3a7a33"],
            hover_color=["#2d5a27", "#2d5a27"],
            command=self.go_to_home
        )
        self.back_button.grid(row=0, column=4, pady=20, padx=20, sticky="e")
        
        # Chat area
        self.chat_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=["#242424", "#242424"],
            corner_radius=15
        )
        self.chat_frame.grid(row=1, column=0, pady=(10, 5), padx=20, sticky="nsew")
        self.chat_frame.grid_columnconfigure(0, weight=1)
        
        # Input area frame
        self.input_frame = ctk.CTkFrame(
            self, 
            fg_color=["#2b2b2b", "#2b2b2b"],
            corner_radius=15
        )
        self.input_frame.grid(row=2, column=0, pady=(5, 20), padx=20, sticky="ew")
        self.input_frame.grid_columnconfigure(0, weight=1)
        
        # Entry field
        self.entry = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="Type your argument here...",
            height=45,
            font=("Helvetica", 14),
            corner_radius=10,
            fg_color=["#333333", "#333333"],
            border_color=["#3a7a33", "#3a7a33"],
            border_width=2,
            text_color="white"
        )
        self.entry.grid(row=0, column=0, pady=15, padx=(15, 10), sticky="ew")
        
        # Submit button
        self.submit_button = ctk.CTkButton(
            self.input_frame,
            text="Send",
            width=100,
            height=45,
            corner_radius=10,
            font=("Helvetica", 14, "bold"),
            fg_color=["#3a7a33", "#3a7a33"],
            hover_color=["#2d5a27", "#2d5a27"],
            command=self.send_message
        )
        self.submit_button.grid(row=0, column=1, pady=15, padx=(0, 15))
        
        # Bind Enter key
        self.entry.bind("<Return>", lambda event: self.send_message())

    def go_to_home(self):
        globals.chat_messages.clear()
        self.controller.show_frame(self.controller.frames["HomePage"])

    def send_message(self):
        user_text = self.entry.get()
        if user_text:
            chat_bubble = ChatBubble(self.chat_frame, user_text, align="right")
            chat_bubble.pack(anchor="e", fill="y", expand=False, padx=0, pady=0)
            self.entry.delete(0, ctk.END)
            # globals.ask(user_text)
            threading.Thread(target=self.fetch_opponent_response, args=(user_text,), daemon=True).start()

    def fetch_opponent_response(self, user_text):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.opponent_response(user_text))

    async def opponent_response(self, user_text):
        start_time = time.time()
        chat_bubble = ChatBubble(self.chat_frame, f"Thinking of a response...", align="left")
        chat_bubble.pack(anchor="w", fill="y", expand=False, padx=0, pady=0)
        suggestion_bubble = CollapsibleSuggestionBubble(self.chat_frame, "Analyzing argument...")
        suggestion_bubble.pack(anchor="w", fill="y", expand=False, padx=0, pady=0)

        print("Thinking...")
        self.response = self.controller.manager.process_argument(self.debate_id, user_text)
        print(self.response)
        
        chat_bubble.update_text(self.response["ai_argument"])
        suggestion_bubble.update_text(self.response["evaluation_feedback"])
        end_time = time.time()
        time_taken = round(end_time - start_time, 2)
        self.user_score += (self.response["score"] * 100)
        self.opponent_score += (self.response["ai_score"] * 100)
        self.user_score_label.configure(text=f"Your Score: {self.user_score}")
        self.opponent_score_label.configure(text=f"Opponent's Score: {self.opponent_score}")

        thought_time_label = ctk.CTkLabel(
            self.chat_frame, 
            text=f"🤔 Thought for {time_taken} seconds", 
            font=("Helvetica", 12, "italic"),
            text_color=["#aaaaaa", "#aaaaaa"]
        )
        thought_time_label.pack(anchor="w", padx=10, pady=5)
        # globals.respond(response_text)