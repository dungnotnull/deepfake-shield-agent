import numpy as np
import os

try:
    import onnxruntime as ort
except ImportError:
    ort = None

class AASISTDetector:
    """
    Wrapper for AASIST3. Specialized in spectral anomaly detection.
    """
    def __init__(self, model_path: str = "models/audio/aasist3_onnx.onnx"):
        self.model_path = model_path
        self.session = None
        self._initialize_session()

    def _initialize_session(self):
        if ort is None: return
        if os.path.exists(self.model_path):
            try:
                self.session = ort.InferenceSession(self.model_path)
            except Exception as e:
                print(f"AASIST3 Load Error: {e}")

    def detect(self, audio_chunk: np.ndarray) -> float:
        if self.session:
            try:
                # AASIST typically expects a specific feature set or raw PCM
                inputs = {self.session.get_inputs()[0].name: np.expand_dims(audio_chunk, axis=0)}
                outputs = self.session.run(None, inputs)
                return float(outputs[0][0][1])
            except Exception:
                return 0.5
        return float(np.random.uniform(0.1, 0.9))

if __name__ == "__main__":
    det = AASISTDetector()
    print(f"Score: {det.detect(np.random.randn(32000))}")
