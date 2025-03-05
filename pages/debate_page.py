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
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=0)
        
        self.label = ctk.CTkLabel(self, text=f"Debate Room - {self.debate_opponent}", font=("Arial", 30))
        self.label.grid(row=0, column=0, pady=10, padx=10, sticky="nsew")
        
        self.chat_frame = ctk.CTkScrollableFrame(self)
        self.chat_frame.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")
        self.chat_frame.grid_columnconfigure(0, weight=1)
        self.chat_frame.grid_rowconfigure(0, weight=1)
        
        self.entry = ctk.CTkEntry(self, placeholder_text="Enter your argument")
        self.entry.grid(row=2, column=0, pady=5, padx=10, sticky="ew")
        
        self.submit_button = ctk.CTkButton(self, text="Send", command=self.send_message)
        self.submit_button.grid(row=3, column=0, pady=10, padx=10, sticky="ew")
    
    def send_message(self):
        user_text = self.entry.get()
        if user_text:
            chat_bubble = ChatBubble(self.chat_frame, user_text, align="right")
            chat_bubble.pack(anchor="e", fill="y", expand=True, padx=10, pady=5)
            self.entry.delete(0, ctk.END)
            globals.ask(user_text)
            # Start a new thread to fetch the response asynchronously
            threading.Thread(target=self.fetch_opponent_response, args=(user_text,), daemon=True).start()

    def fetch_opponent_response(self, user_text):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.opponent_response(user_text))

    async def opponent_response(self, user_text):
        chat_bubble = ChatBubble(self.chat_frame, f"{self.debate_opponent} is thinking...", align="left")
        chat_bubble.pack(anchor="w", fill="y", expand=True, padx=10, pady=5)
        judge_bubble = ChatBubble(self.chat_frame, f"Judge is thinking...", align="left")
        judge_bubble.pack(anchor="w", fill="y", expand=True, padx=10, pady=5)
        response_text = ""
        judge_text = ""
        print(globals.chat_messages)
        ollama_session = ollama.chat(model="llama2-uncensored", messages=globals.chat_messages, stream=True)
        print("In ollama session")
        judge_session = ollama.chat(model="sadiq-bd/llama3.2-1b-uncensored", messages=[{"role": "system", "content": f"You are an impartial debate judge who evaluates arguments objectively. Your task is to provide brief, constructive feedback (2-3 sentences) on how the argument could be improved. The user is currently debating against {self.debate_opponent}. Stay neutral and avoid taking a stance. Identify logical strengths and weaknesses concisely. Point out any logical fallacies in a single sentence if present. Suggest 1-2 quick improvements without changing the user’s stance. Keep your response to 2-3 lines only for clarity. "},
                                                                   {"role": "user", "content": user_text}], stream=True)
        print("In judge session")
        for chunk in ollama_session:
            response_text += chunk["message"]["content"]
            chat_bubble.update_text(response_text)

        for chunk in judge_session:
            judge_text += chunk["message"]["content"]
            judge_bubble.update_text(judge_text)

        
        chat_bubble.update_text(response_text)  # Ensure the final text is set
        judge_bubble.update_text(judge_text)
        globals.respond(response_text)
