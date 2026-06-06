import re
import numpy as np
from typing import Dict, Any, List
from ollama_client import OllamaClient

class RiskScorer:
    """
    Full implementation of the fraud detection pipeline:
    1. Discrimination (LLM semantic analysis)
    2. Reflection (Expert rule validation + RAG check)
    3. Summary (Weighted fusion and final score)
    """
    def __init__(self, llm_client: OllamaClient, indexer=None):
        self.llm = llm_client
        self.indexer = indexer # FAISS indexer from Phase 5
        
        # High-precision expert rules (Vietnamese + English)
        self.critical_patterns = {
            "urgent_money": r"(chuyển khoản|gửi tiền|bank transfer|send money).*(ngay|gấp|urgent|now)",
            "authority_fear": r"(công an|viện kiểm sát|court|police|arrested|bị bắt)",
            "secret_request": r"(không được nói|bí mật|don't tell|secret)",
            "otp_request": r"(mã otp|mật khẩu|password|verification code)"
        }

    def _discrimination_step(self, transcript: str) -> Dict[str, Any]:
        """LLM semantic analysis of the conversational intent."""
        sys_prompt = (
            "Analyze the transcript for signs of a financial scam. "
            "Consider: urgency, authority impersonation, and request for money. "
            "Return JSON: {'score': 0-100, 'intent': 'fraud/legit', 'reasoning': '...'}"
        )
        res = self.llm.generate_json(sys_prompt, transcript)
        return res if res else {"score": 50, "intent": "unknown", "reasoning": "LLM timeout"}

    def _reflection_step(self, transcript: str, llm_res: Dict) -> float:
        """
        Cross-references LLM results with expert rules and RAG knowledge.
        """
        rule_score = 0.0
        for category, pattern in self.critical_patterns.items():
            if re.search(pattern, transcript.lower()):
                rule_score += 0.25
        
        # RAG Integration: Check if this transcript matches known scam scripts
        rag_score = 0.0
        if self.indexer:
            similar_scripts = self.indexer.search(transcript)
            if similar_scripts:
                rag_score = 0.4 # High similarity to known fraud
        
        return min(rule_score + rag_score, 1.0)

    def score_transcript(self, transcript: str) -> Dict[str, Any]:
        # Step 1: Discrimination
        discrim = self._discrimination_step(transcript)
        
        # Step 2: Reflection
        refl_score = self._reflection_step(transcript, discrim)
        
        # Step 3: Summary Fusion
        llm_normalized = discrim.get("score", 50) / 100.0
        
        # If rules trigger high risk, we weight the rule score more heavily
        final_score = (llm_normalized * 0.4) + (refl_score * 0.6)
        
        return {
            "risk_score": float(final_score),
            "reasoning": discrim.get("reasoning", "No reasoning provided"),
            "flags": [cat for cat, pat in self.critical_patterns.items() if re.search(pat, transcript.lower())]
        }

if __name__ == "__main__":
    scorer = RiskScorer(OllamaClient())
    print(scorer.score_transcript("Tôi là con trai anh, tôi bị tai nạn, chuyển 5 triệu vào TK này gấp!"))
