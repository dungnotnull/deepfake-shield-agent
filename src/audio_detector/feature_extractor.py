import numpy as np
import librosa
from typing import Dict, Any

class AudioFeatureExtractor:
    """
    Production-grade extractor for audio anti-spoofing.
    Implements MFCCs, Mel-spectrograms, and Spectral Centroid.
    """
    def __init__(self, sample_rate=16000, n_mfcc=80, n_mels=128):
        self.sample_rate = sample_rate
        self.n_mfcc = n_mfcc
        self.n_mels = n_mels

    def preprocess(self, audio_chunk: np.ndarray) -> np.ndarray:
        """Normalization and silence removal."""
        # Normalize audio to [-1, 1]
        max_val = np.max(np.abs(audio_chunk))
        if max_val > 0:
            audio_chunk = audio_chunk / max_val
        
        # Simple voice activity detection (VAD) - discard if too quiet
        if np.sqrt(np.mean(audio_chunk**2)) < 0.01:
            return None
            
        return audio_chunk

    def extract(self, audio_chunk: np.ndarray) -> Dict[str, np.ndarray]:
        """
        Full extraction pipeline.
        """
        processed = self.preprocess(audio_chunk)
        if processed is None:
            return {}

        # 1. MFCCs: Essential for capturing vocal tract characteristics
        mfccs = librosa.feature.mfcc(y=processed, sr=self.sample_rate, n_mfcc=self.n_mfcc)
        
        # 2. Mel-spectrogram: Captures frequency-domain artifacts of TTS
        mel_spec = librosa.feature.melspectrogram(y=processed, sr=self.sample_rate, n_mels=self.n_mels)
        mel_db = librosa.power_to_db(mel_spec, ref=np.max)
        
        # 3. Spectral Centroid: Detects 'brightness' / high-freq noise in deepfakes
        centroid = librosa.feature.spectral_centroid(y=processed, sr=self.sample_rate)
        
        return {
            "mfcc": mfccs,
            "mel_spec": mel_db,
            "spectral_centroid": centroid,
            "raw_pcm": processed
        }

if __name__ == "__main__":
    extractor = AudioFeatureExtractor()
    dummy = np.random.uniform(-1, 1, 16000 * 2)
    feats = extractor.extract(dummy)
    print(f"Extracted features: {list(feats.keys())}")
