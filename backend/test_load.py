from llama_cpp import Llama
import os

# Paste your absolute path here
model_path = r".\models\Meta-Llama-3-8B-Instruct.Q4_K_S.gguf" 

print(f"1. Checking if file physically exists: {os.path.exists(model_path)}")

try:
    print("2. Attempting to load model into RAM...")
    llm = Llama(model_path=model_path, verbose=True)
    print("3. SUCCESS! The brain is loaded.")
except Exception as e:
    print(f"3. FAILED: {e}")