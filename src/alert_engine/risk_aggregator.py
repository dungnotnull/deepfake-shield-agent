from typing import Dict, List, Optional
import numpy as np
import time

class RiskAggregator:
    """
    The core decision engine of the system.
    Implements multimodal fusion and temporal risk decay.
    """
    def __init__(self, window_sec: int = 30):
        self.window_sec = window_sec
        self.score_history = [] # List of (timestamp, fused_score)

    def _update_history(self, score: float):
        now = time.time()
        self.score_history.append((now, score))
        # Cleanup old scores
        self.score_history = [s for s in self.score_history if now - s[0] < self.window_sec]

    def fuse(self, audio: float, video: float, text: float) -> Dict[str, Any]:
        """
        Multimodal Fusion Logic.
        Weights: Audio (40%), Video (40%), Text (20%).
        """
        # 1. Basic Weighted Average
        fused = (audio * 0.4) + (video * 0.4) + (text * 0.2)
        
        # 2. Critical Override: If any modality is extremely confident (>0.95), 
        # the overall risk is immediately pushed to ALERT level.
        max_signal = max(audio, video, text)
        if max_signal > 0.95:
            fused = max(fused, 0.9)

        # 3. Temporal Smoothing (EMA)
        self._update_history(fused)
        smoothed_score = np.mean([s[1] for s in self.score_history])
        
        # 4. Level Mapping
        level = "NORMAL"
        if smoothed_score > 0.75:
            level = "ALERT"
        elif smoothed_score > 0.45:
            level = "WARN"
            
        return {
            "score": float(smoothed_score),
            "level": level,
            "contributions": {"audio": audio, "video": video, "text": text}
        }

if __name__ == "__main__":
    agg = RiskAggregator()
    print(agg.fuse(0.8, 0.1, 0.9))
