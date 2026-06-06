from typing import List, Optional
from ollama_client import OllamaClient

class ChallengeEngine:
    """
    Generates unpredictable, context-aware verification questions.
    """
    def __init__(self, llm_client: OllamaClient):
        self.llm = llm_client

    def generate_challenge(self, transcript: str, risk_level: str) -> Optional[str]:
        """
        Produces a question that requires specific shared memory.
        """
        if risk_level == "NORMAL":
            return None
            
        sys_prompt = (
            "You are a security agent. Generate a challenging question based on the "
            "conversation context that only a real family member or friend would know. "
            "The question must be specific and NOT answerable by a general AI."
        )
        
        res = self.llm.generate_json(sys_prompt, f"Context: {transcript}")
        if res and "question" in res:
            return res["question"]
            
        # Fallback templates
        fallbacks = [
            "What was the name of our first pet together?",
            "Where did we go for our last holiday?",
            "What is my mother's maiden name?"
        ]
        import random
        return random.choice(fallbacks)

if __name__ == "__main__":
    engine = ChallengeEngine(OllamaClient())
    print(engine.generate_challenge("Caller claims to be son in emergency", "ALERT"))
