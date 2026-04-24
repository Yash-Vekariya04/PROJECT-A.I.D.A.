from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
# Import your custom modules!
from brain import AidaBrain
from router import AidaRouter
from tools import AidaTools
from voice import AidaVoice
import json
import requests

app = FastAPI()

# --- ENTIRE SECURITY BLOCK ---
# This tells the server to accept connections from your browser
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # Explicitly allows Port 3000 to connect
    allow_credentials=False,   # Must be False when using the "*" wildcard
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. Boot the AI components when the server starts
print("[SYSTEM] Initializing Core Architecture...")
router = AidaRouter()
tools = AidaTools()
voice_engine = AidaVoice()

# Make sure to point this to your actual downloaded .gguf file
brain = AidaBrain(model_path=r".\models\Meta-Llama-3-8B-Instruct.Q4_K_S.gguf") 

@app.websocket("/ws/aida")
async def friday_websocket(websocket: WebSocket):
    await websocket.accept()
    print("[SYSTEM] The sWebSocket door is opened...")
    print("[SYSTEM] Holographic Interface Connected. A.I.D.A is online.")
    
    try:
        while True:
            user_text = await websocket.receive_text()
            print(f"[USER]: {user_text}")
            
            # 2. Talk to Ollama (Quantized Llama 3)
            ollama_response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "llama3",
                    "prompt": user_text,
                    "stream": False # We'll set this to True when we do streaming!
                }
            )
            
            ai_response = ollama_response.json().get("response")
            print(f"[AIDA]: {ai_response}")
            
            # 3. Generate voice as usual
            audio_base64 = await voice_engine.generate_audio_base64(ai_response)
            
            # 4. Send to UI
            payload = {
                "text": ai_response,
                "mood": "default",
                "audio_data": audio_base64
            }
            await websocket.send_text(json.dumps(payload))

    except WebSocketDisconnect:
        print("[SYSTEM] Interface disconnected. Returning to standby.")
