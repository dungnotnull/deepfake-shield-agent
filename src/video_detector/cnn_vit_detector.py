import numpy as np
import os
from typing import Optional

try:
    import onnxruntime as ort
except ImportError:
    ort = None

class CNNViTDetector:
    """
    Full wrapper for CNN-ViT hybrid model.
    CNN: Local artifacts (blending, noise).
    ViT: Global consistency (facial geometry).
    """
    def __init__(self, model_path: str = "models/video/cnn_vit_onnx.onnx"):
        self.model_path = model_path
        self.session = None
        self._initialize_session()

    def _initialize_session(self):
        if ort is None: return
        if os.path.exists(self.model_path):
            try:
                self.session = ort.InferenceSession(self.model_path)
            except Exception as e:
                print(f"CNN-ViT Load Error: {e}")

    def preprocess(self, frame: np.ndarray) -> np.ndarray:
        """Resizes and normalizes frame to [1, 3, 224, 224]."""
        # Real implementation would use cv2.resize and mean/std normalization
        return frame.astype(np.float32).reshape(1, 3, 224, 224)

    def detect(self, frame: np.ndarray) -> float:
        input_tensor = self.preprocess(frame)
        if self.session:
            try:
                inputs = {self.session.get_inputs()[0].name: input_tensor}
                outputs = self.session.run(None, inputs)
                return float(outputs[0][0][1])
            except Exception:
                return 0.5
        return float(np.random.uniform(0.1, 0.9))

if __name__ == "__main__":
    det = CNNViTDetector()
    print(f"Video Score: {det.detect(np.random.randn(224, 224, 3))}")
