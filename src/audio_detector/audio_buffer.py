import collections
import numpy as np
from typing import Optional

class AudioBuffer:
    """
    Real-time sliding window manager for audio streams.
    Ensures continuous analysis without gaps.
    """
    def __init__(self, sample_rate: int = 16000, window_sec: float = 2.0, overlap_sec: float = 0.512):
        self.sample_rate = sample_rate
        self.window_size = int(window_sec * sample_rate)
        self.overlap_size = int(overlap_sec * sample_rate)
        self.step_size = self.window_size - self.overlap_size
        
        # The internal buffer stores incoming raw samples
        self.buffer = collections.deque()

    def push(self, samples: np.ndarray):
        """Push new samples from the proxy layer."""
        self.buffer.extend(samples)

    def pop_window(self) -> Optional[np.ndarray]:
        """
        Returns a full window if available and slides the buffer.
        Returns None if not enough samples have accumulated.
        """
        if len(self.buffer) < self.window_size:
            return None
            
        # Extract window
        window = np.array(list(self.buffer)[:self.window_size])
        
        # Slide the buffer by step_size
        for _ in range(self.step_size):
            if self.buffer:
                self.buffer.popleft()
                
        return window

if __name__ == "__main__":
    buf = AudioBuffer()
    # Simulate 1 second of audio (16k samples)
    buf.push(np.random.randn(16000))
    print(f"Window 1: {buf.pop_window()}") # Should be None (needs 32k)
    buf.push(np.random.randn(16000))
    print(f"Window 2: {buf.pop_window() is not None}") # Should be True
