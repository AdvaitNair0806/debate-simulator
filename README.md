# Debate Simulator

An AI-powered **debate simulator** where users can engage in **live debates** with an AI opponent, receive **argument analysis**, and get responses in real-time. Ideas taken from https://arxiv.org/abs/2412.06229

---

## 🚀 Features  
✅ **Live AI Debates** – Argue with AI opponents that adapt to your reasoning style  
✅ **Argument Analysis** – AI evaluates argument strength and suggests improvements  
✅ **Adversarial Search** – Predicts and counters your debate style (logical, emotional, counterexamples)  
✅ **CustomTkinter UI** – Modern, dark-themed interface with collapsible feedback sections  

---

## 🛠️ Tech Stack  
- **Frontend**: `CustomTkinter` (modern UI for Python)  
- **AI Models**: `Ollama` (Llama, Gemma, Phi)  
- **Backend**: `Python (async, threading, asyncio)`  
- **Logic**: Genetic algorithms for argument generation  

---

## 📦 Installation  

### 1️⃣ Clone the repository  
```bash
git clone https://github.com/your-repo/debate-simulator.git
cd debate-simulator
```

### 2️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Pull the required models
```bash
ollama pull gemma3:1b
ollama pull llama3.2:1b
ollama pull phi3.5:latest
```

### 4️⃣ Run the application
```bash
python main.py
```