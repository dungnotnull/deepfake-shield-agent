import time
import numpy as np
from audio_detector.audio_ensemble import AudioEnsemble
from video_detector.video_ensemble import VideoEnsemble
from transcript_agent.risk_scorer import RiskScorer
from transcript_agent.ollama_client import OllamaClient

def benchmark():
    print("--- Running Latency Benchmark ---")
    
    # Audio
    start = time.time()
    AudioEnsemble().process_chunk(np.random.randn(32000))
    print(f"Audio Inference: {(time.time()-start)*1000:.2f}ms")
    
    # Video
    start = time.time()
    VideoEnsemble().process_frame(np.random.randn(224,224,3), None, [], [])
    print(f"Video Inference: {(time.time()-start)*1000:.2f}ms")
    
    # LLM
    start = time.time()
    RiskScorer(OllamaClient()).score_transcript("Test scam transcript")
    print(f"LLM Scoring: {(time.time()-start)*1000:.2f}ms")

if __name__ == "__main__":
    benchmark()
