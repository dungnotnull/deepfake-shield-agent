from typing import List, Dict, Tuple
import numpy as np

class AudioEnsemble:
    """
    Production-grade fusion of audio detectors.
    Implements: Weighted Averaging, Confidence-based Gating, and Temporal Smoothing.
    """
    def __init__(self, config: Dict[str, float] = None):
        # config: {"wav2vec": 0.6, "aasist": 0.4}
        self.weights = config if config else {"wav2vec": 0.6, "aasist": 0.4}
        
        # Actual model instances
        from wav2vec_detector import Wav2VecDetector
        from aasist_detector import AASISTDetector
        self.models = {
            "wav2vec": Wav2VecDetector(),
            "aasist": AASISTDetector()
        }
        
        # Temporal smoothing buffer
        self.score_history = []
        self.history_max = 10

    def fuse_scores(self, scores: Dict[str, float]) -> float:
        """
        Weighted fusion with confidence gating.
        If any model is extremely confident (>0.95), it can override the average.
        """
        weighted_sum = 0.0
        total_weight = 0.0
        
        for model_id, score in scores.items():
            # Gating: Overwhelming evidence of fake
            if score > 0.98:
                return 1.0 
            
            weight = self.weights.get(model_id, 0.5)
            weighted_sum += score * weight
            total_weight += weight
            
        return weighted_sum / total_weight if total_weight > 0 else 0.5

    def process_chunk(self, audio_chunk: np.ndarray) -> float:
        """
        End-to-end chunk processing: Inference -> Fusion -> Smoothing.
        """
        # 1. Get individual scores
        scores = {m_id: model.detect(audio_chunk) for m_id, model in self.models.items()}
        
        # 2. Fuse
        fused = self.fuse_scores(scores)
        
        # 3. Temporal Smoothing (EMA - Exponential Moving Average)
        self.score_history.append(fused)
        if len(self.score_history) > self.history_max:
            self.score_history.pop(0)
            
        smoothed_score = np.mean(self.score_history)
        return float(smoothed_score)

if __name__ == "__main__":
    ensemble = AudioEnsemble()
    print(f"Smoothed Audio Score: {ensemble.process_chunk(np.random.randn(32000))}")
