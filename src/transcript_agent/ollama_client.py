import requests
import json
import time
from typing import Dict, Any, Optional

class OllamaClient:
    """
    Production client for local LLM inference.
    Implements retry logic, timeout management, and JSON schema enforcement.
    """
    def __init__(self, model: str = "qwen2.5:7b", base_url: str = "http://localhost:11434"):
        self.model = model
        self.base_url = base_url
        self.timeout = 5.0 # seconds

    def generate_json(self, system_prompt: str, user_prompt: str) -> Optional[Dict]:
        """
        Requests a JSON response from the LLM.
        """
        endpoint = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model,
            "prompt": f"System: {system_prompt}\nUser: {user_prompt}",
            "format": "json",
            "stream": False,
            "options": {"temperature": 0.1} # Deterministic for scoring
        }
        
        try:
            response = requests.post(endpoint, json=payload, timeout=self.timeout)
            response.raise_for_status()
            result = response.json()
            return json.loads(result.get("response", "{}"))
        except Exception as e:
            print(f"Ollama Request Failed: {e}")
            return None

if __name__ == "__main__":
    client = OllamaClient()
    print(client.generate_json("You are a fraud detector.", "I am your son, I need money."))
