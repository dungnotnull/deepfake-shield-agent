from typing import Dict, List
import numpy as np

class VideoEnsemble:
    """
    Production fusion for video channels.
    Priority Logic: Active probe 'Success' (High match) can override passive artifacts.
    """
    def __init__(self):
        from cnn_vit_detector import CNNViTDetector
        from active_probe import ActiveProbeDetector
        self.passive_model = CNNViTDetector()
        self.active_model = ActiveProbeDetector()

    def fuse(self, passive_score: float, active_score: float) -> float:
        """
        Fuses passive forgery score and active probe confidence.
        Note: active_score is 'Confidence in Human' (1.0 = Human).
        Passive_score is 'Probability of Fake' (1.0 = Fake).
        """
        # If active probe is highly confident it is a human (active_score > 0.9),
        # we heavily penalize the passive score to reduce false positives.
        if active_score > 0.9:
            return passive_score * 0.2
        
        # If active probe is low (cannot find reflection), we rely on passive.
        if active_score < 0.3:
            return passive_score * 1.2 # Increase risk
            
        # Balanced fusion
        return (passive_score * 0.7) + ((1 - active_score) * 0.3)

    def process_frame(self, frame: np.ndarray, landmarks: np.ndarray, eye_crops: List[np.ndarray], gaze_hist: List[np.ndarray]) -> float:
        p_score = self.passive_model.detect(frame)
        a_score = self.active_model.verify_corneal_reflection(eye_crops)
        g_score = self.active_model.verify_gaze_consistency(gaze_hist)
        
        # Average the two active probes
        combined_active = (a_score + g_score) / 2.0
        
        return self.fuse(p_score, combined_active)

if __name__ == "__main__":
    ens = VideoEnsemble()
    print(f"Fused Video Score: {ens.process_frame(np.random.randn(224,224,3), None, [], [])}")
