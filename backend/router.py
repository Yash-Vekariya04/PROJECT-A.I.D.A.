class AidaRouter:
    def __init__(self):
        # 1. The Prompt Vault
        # This is where we store the different "scripts" F.R.I.D.A.Y. can read from.
        self.personas = {
            "academic": """SYSTEM: You are A.I.D.A., operating in Academic Tutor mode. 
            Your tone is strict, precise, and highly mathematical. Challenge the user to think critically.""",
            
            "casual": """SYSTEM: You are A.I.D.A., operating in Casual mode. 
            Your tone is relaxed, shy, soothing, and slightly witty. Treat the user like a close friend.""",
            
            "default": """SYSTEM: You are A.I.D.A., an advanced digital assistant. 
            Your tone is professional, concise, and calming. Get straight to the point."""
        }
        
        # 2. The Triggers
        # Lists of words that define the "vibe" of the conversation.
        self.academic_keywords = ["math", "theorem", "study", "gate", "calculus", "probability", "code", "algorithm"]
        self.casual_keywords = ["tired", "joke", "movie", "exhausted", "relax", "chill", "sleep", "bored"]

    def analyze_mood(self, user_text: str):
        """
        Scans the user's text and returns the appropriate System Prompt and a status label.
        """
        # Convert everything to lowercase so "Math" and "math" trigger the same way
        text = user_text.lower()
        
        # Check for Academic context
        if any(word in text for word in self.academic_keywords):
            return self.personas["academic"], "Academic"
            
        # Check for Casual context
        elif any(word in text for word in self.casual_keywords):
            return self.personas["casual"], "Casual"
            
        # Fallback to normal behavior
        else:
            return self.personas["default"], "Standard"


# ==========================================
# INTERACTIVE TESTING BLOCK
# ==========================================
# This allows you to run `python router.py` in your terminal to test the logic.
if __name__ == "__main__":
    router = AidaRouter()
    print("========================================")
    print("F.R.I.D.A.Y. Context Router Online.")
    print("Type a message to test the routing logic.")
    print("Type 'exit' to shut down.")
    print("========================================\n")
    
    while True:
        user_input = input("You: ")
        
        if user_input.lower() == 'exit':
            print("Shutting down router...")
            break
            
        # Pass the input into the algorithm
        selected_prompt, detected_mood = router.analyze_mood(user_input)
        
        # Display what the system decided
        print(f"\n---> [SYSTEM] Mood Detected: {detected_mood}")
        print(f"---> [INJECTED SCRIPT]: {selected_prompt}\n")