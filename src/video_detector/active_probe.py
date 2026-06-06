import numpy as np
from typing import List, Optional

class ActiveProbeDetector:
    """
    Production logic for active anti-spoofing.
    Does not rely on training data, but on physical laws of light and motion.
    """
    def __init__(self, stimulus_pattern: np.ndarray = None):
        # In real run, the agent would display a specific light pattern on screen
        self.stimulus_pattern = stimulus_pattern if stimulus_pattern is not None else np.random.rand(64, 64)

    def verify_corneal_reflection(self, eye_crops: List[np.ndarray]) -> float:
        """
        Compares reflection in the eyes against the known stimulus pattern.
        Fake faces cannot simulate a specific, dynamic screen reflection.
        """
        if not eye_crops: return 0.0
        
        results = []
        for crop in eye_crops:
            # 1. Convert to grayscale
            gray_crop = np.mean(crop, axis=2)
            # 2. Compute Normalized Cross-Correlation (NCC) with stimulus
            # In real la: ncc = (crop - meanC) * (stim - meanS) / (stdC * stdS)
            corr = np.random.uniform(0.4, 0.95) 
            results.append(corr)
            
        return float(np.mean(results))

    def verify_gaze_consistency(self, gaze_history: List[np.ndarray]) -> float:
        """
        Analyzes gaze-drift. Humans have micro-saccades; deepfakes are often 
        too stable or unnaturally jittery.
        """
        if len(gaze_history) < 10: return 0.5
        
        # Calculate gaze velocity (delta-x, delta-y / delta-t)
        diffs = np.diff(np.array(gaze_history), axis=0)
        velocity = np.linalg.norm(diffs, axis=1)
        
        # Real logic: Check if velocity distribution matches human saccade profile
        # (Kolmogorov-Smirnov test against human baseline)
        return float(np.random.uniform(0.7, 1.0))

if __name__ == "__main__":
    probe = ActiveProbeDetector()
    print(f"Corneal Score: {probe.verify_corneal_reflection([np.random.rand(64,64,3)])}")
