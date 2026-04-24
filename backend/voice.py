import edge_tts
import base64

class AidaVoice:
    def __init__(self):
        # "en-US-AriaNeural" is a highly natural, soft female voice
        # Other good options: "en-US-AnaNeural" or "en-GB-SoniaNeural"
        self.voice = "en-US-AriaNeural" 
        
    async def generate_audio_base64(self, text: str) -> str:
        """Takes text, generates MP3 audio in memory, and returns a base64 string."""
        print("[SYSTEM] Synthesizing A.I.D.A.'s Voice...")
        
        communicate = edge_tts.Communicate(text, self.voice)
        audio_bytes = b""
        
        # Stream the audio chunks directly into memory
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_bytes += chunk["data"]
        
        # Encode the bytes into a string so it can be packaged in JSON
        return base64.b64encode(audio_bytes).decode('utf-8')