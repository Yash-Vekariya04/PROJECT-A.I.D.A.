from llama_cpp import Llama

class AidaBrain:
    def __init__(self, model_path: str):
        """
        Initializes the F.R.I.D.A.Y. neural network using a quantized GGUF model.
        """
        print(f"[SYSTEM] Booting Neural Engine from {model_path}...")
        
        # We load the model with a 2048 token context window.
        # n_gpu_layers=0 means it runs entirely on the CPU (perfect for a Pi).
        try:
            self.llm = Llama(
                model_path=model_path,
                n_ctx=2048,          # Maximum sequence length
                n_threads=4,         # Adjust based on your CPU cores
                n_gpu_layers=0,      # Set >0 if you have a dedicated GPU
                verbose=False        # Hides the underlying C++ matrix math logs
            )
            print("[SYSTEM] Neural Engine Online.")
        except Exception as e:
            print(f"[ERROR] Failed to load the brain: {e}")
            self.llm = None

    def generate_response(self, user_text: str, system_prompt: str = "") -> str:
        """
        Passes the user's text into the LLM and returns the generated string.
        """
        if not self.llm:
            return "Error: Brain is offline."

        # The ChatML format: How modern models separate system instructions from user input
        prompt_template = f"""<|im_start|>system
            {system_prompt}<|im_end|>
            <|im_start|>user
            {user_text}<|im_end|>
            <|im_start|>assistant
            """
        
        # The Autoregressive Generation Loop (from Phase 3.4)
        response = self.llm(
            prompt_template,
            max_tokens=150,      # Limit how much she speaks to keep latency low
            temperature=0.7,     # The "Creativity" knob (0.7 is a good conversational mix)
            stop=["<|im_end|>"], # Stop generating when the sentence is mathematically finished
            echo=False           # Don't repeat the prompt back to us
        )
        
        # Extract the exact string from the JSON response object
        output_text = response['choices'][0]['text'].strip()
        return output_text

# ==========================================
# LOCAL TESTING BLOCK
# ==========================================
# This code only runs if you execute this file directly, 
# not if you import it into server.py
if __name__ == "__main__":
    # 1. You must download a .gguf model file and put it in your 'models' folder
    # Example: "Phi-3-mini-4k-instruct-q4.gguf" (A highly capable, tiny model)
    MODEL_FILE = r"C:\Users\yashv\OneDrive\Desktop\Yash\Dev\ML\FRIDAY\FRIDAY\backend\models\Meta-Llama-3-8B-Instruct.Q4_K_S.gguf" 
    
    # Define F.R.I.D.A.Y.'s personality and tools
    FRIDAY_PROMPT = """You are F.R.I.D.A.Y., an advanced AI assistant. 
        Keep your answers concise, helpful, and slightly formal."""

    # Boot the brain
    brain = AidaBrain(model_path=MODEL_FILE)
    
    # Test the inference
    test_query = "What is the capital of Japan, and how long is the flight from India?"
    print(f"\n[USER]: {test_query}")
    
    answer = brain.generate_response(test_query, system_prompt=FRIDAY_PROMPT)
    print(f"[FRIDAY]: {answer}\n")