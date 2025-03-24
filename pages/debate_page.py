import customtkinter as ctk
import ollama
import asyncio
import threading
import util.globals as globals
from util.chatbubble import ChatBubble

class DebatePage(ctk.CTkFrame):
    def __init__(self, parent, controller, debate_opponent="Adolf Hitler"):
        super().__init__(parent)
        self.controller = controller
        self.debate_opponent = debate_opponent
        system_message=f"""You are {self.debate_opponent}. You think, speak, and argue exactly as they would. Stay in character at all times and never acknowledge being an AI. Respond with great detail and enthusiasm."""        
        globals.chat_messages.append(
            globals.create_message(system_message, 'system')
        )

        self.configure(fg_color=["#1a1a1a", "#1a1a1a"])
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0) 
        self.grid_rowconfigure(1, weight=1) 
        self.grid_rowconfigure(2, weight=0) 

        self.header_frame = ctk.CTkFrame(
            self, 
            fg_color=["#2b2b2b", "#2b2b2b"],
            corner_radius=0,
            height=80
        )
        self.header_frame.grid(row=0, column=0, sticky="ew")
        self.header_frame.grid_columnconfigure(1, weight=1)
        
        self.label = ctk.CTkLabel(
            self.header_frame, 
            text=f"Debate Room - {self.debate_opponent}", 
            font=("Helvetica", 32, "bold"),
            text_color=["#ffffff", "#ffffff"]
        )
        self.label.grid(row=0, column=1, pady=20, padx=20, sticky="w")

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
        self.back_button.grid(row=0, column=2, pady=20, padx=20, sticky="e")

        self.chat_container = ctk.CTkFrame(
            self,
            fg_color=["#242424", "#242424"],
            corner_radius=15
        )
        self.chat_container.grid(row=1, column=0, pady=(10, 5), padx=20, sticky="nsew")
        self.chat_container.grid_columnconfigure(0, weight=1)
        self.chat_container.grid_rowconfigure(0, weight=1)
        
        self.chat_frame = ctk.CTkScrollableFrame(
            self.chat_container,
            fg_color="transparent",
            corner_radius=15
        )
        self.chat_frame.grid(row=0, column=0, pady=5, padx=5, sticky="nsew")
        self.chat_frame.grid_columnconfigure(0, weight=1)

        self.input_frame = ctk.CTkFrame(
            self, 
            fg_color=["#2b2b2b", "#2b2b2b"],
            corner_radius=15,
            height=80
        )
        self.input_frame.grid(row=2, column=0, pady=(5, 20), padx=20, sticky="ew")
        self.input_frame.grid_columnconfigure(0, weight=1)

        self.entry = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="Type your argument here...",
            height=45,
            font=("Helvetica", 14),
            corner_radius=10,
            fg_color=["#333333", "#333333"],
            border_color=["#3a7a33", "#3a7a33"],
            border_width=2
        )
        self.entry.grid(row=0, column=0, pady=15, padx=(15, 10), sticky="ew")
        
        self.submit_button = ctk.CTkButton(
            self.input_frame,
            text="Send ➤",
            width=100,
            height=45,
            corner_radius=10,
            font=("Helvetica", 14, "bold"),
            fg_color=["#3a7a33", "#3a7a33"],
            hover_color=["#2d5a27", "#2d5a27"],
            command=self.send_message
        )
        self.submit_button.grid(row=0, column=1, pady=15, padx=(0, 15))

        self.entry.bind("<Return>", lambda event: self.send_message())

    def go_to_home(self):
        globals.chat_messages.clear()
        self.controller.show_frame(self.controller.frames["HomePage"])

    def send_message(self):
        user_text = self.entry.get()
        if user_text:
            chat_bubble = ChatBubble(
                self.chat_frame, 
                user_text, 
                align="right",
                fg_color=["#3a7a33", "#3a7a33"],
                text_color=["#ffffff", "#ffffff"]
            )
            chat_bubble.pack(anchor="e", fill="y", expand=True, padx=10, pady=5)
            self.entry.delete(0, ctk.END)
            globals.ask(user_text)
            threading.Thread(target=self.fetch_opponent_response, args=(user_text,), daemon=True).start()

    def fetch_opponent_response(self, user_text):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.opponent_response(user_text))

    async def opponent_response(self, user_text):
        thinking_bubble = ChatBubble(
            self.chat_frame, 
            f"{self.debate_opponent} is thinking...", 
            align="left",
            fg_color=["#424242", "#424242"]
        )
        thinking_bubble.pack(anchor="w", fill="y", expand=True, padx=10, pady=5)
        
        judge_bubble = ChatBubble(
            self.chat_frame, 
            f"Judge is thinking...", 
            align="left",
            fg_color=["#424242", "#424242"]
        )
        judge_bubble.pack(anchor="w", fill="y", expand=True, padx=10, pady=5)
        
        response_text = ""
        judge_text = ""
        
        ollama_session = ollama.chat(model="llama2-uncensored", messages=globals.chat_messages, stream=True)
        judge_session = ollama.chat(
            model="sadiq-bd/llama3.2-1b-uncensored", 
            messages=[
                {
                    "role": "system", 
                    "content": f"You are an impartial debate judge who evaluates arguments objectively. Your task is to provide brief, constructive feedback (2-3 sentences) on how the argument could be improved. The user is currently debating against {self.debate_opponent}. Stay neutral and avoid taking a stance. Identify logical strengths and weaknesses concisely. Point out any logical fallacies in a single sentence if present. Suggest 1-2 quick improvements without changing the user's stance. Keep your response to 2-3 lines only for clarity. "
                },
                {"role": "user", "content": user_text}
            ], 
            stream=True
        )

        for chunk in ollama_session:
            response_text += chunk["message"]["content"]
            thinking_bubble.update_text(response_text)

        for chunk in judge_session:
            judge_text += chunk["message"]["content"]
            judge_bubble.update_text(judge_text)
        
        thinking_bubble.update_text(response_text)
        judge_bubble.update_text(judge_text)
        globals.respond(response_text)