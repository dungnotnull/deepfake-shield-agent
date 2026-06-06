import asyncio
import numpy as np
from typing import Optional, Dict
from audio_detector.audio_ensemble import AudioEnsemble
from video_detector.video_ensemble import VideoEnsemble
from transcript_agent.risk_scorer import RiskScorer
from alert_engine.risk_aggregator import RiskAggregator
from alert_engine.alert_dispatcher import AlertDispatcher
from transcript_agent.ollama_client import OllamaClient

class StreamRouter:
    """
    High-performance async orchestrator.
    Uses internal queues to ensure no frame/chunk is dropped during analysis.
    """
    def __init__(self):
        # Initialize components
        self.audio_pipeline = AudioEnsemble()
        self.video_pipeline = VideoEnsemble()
        self.text_pipeline = RiskScorer(OllamaClient())
        self.aggregator = RiskAggregator()
        self.dispatcher = AlertDispatcher()
        
        # Async Queues for decoupling
        self.audio_queue = asyncio.Queue()
        self.video_queue = asyncio.Queue()
        self.text_queue = asyncio.Queue()

    async def ingest_audio(self, chunk: np.ndarray):
        await self.audio_queue.put(chunk)

    async def ingest_video(self, frame: np.ndarray):
        await self.video_queue.put(frame)

    async def ingest_text(self, text: str):
        await self.text_queue.put(text)

    async def worker_loop(self):
        """
        Main processing loop. Synchronizes signals from all three queues.
        """
        print("StreamRouter: Worker loop started.")
        while True:
            # Get latest available data from queues (Non-blocking)
            audio = await self.audio_queue.get() if not self.audio_queue.empty() else None
            video = await self.video_queue.get() if not self.video_queue.empty() else None
            text = await self.text_queue.get() if not self.text_queue.empty() else None
            
            # Process if we have any signal
            if audio is not None or video is not None or text is not None:
                # 1. Get Scores
                a_score = self.audio_pipeline.process_chunk(audio) if audio is not None else 0.0
                v_score = self.video_pipeline.process_frame(video, None, [], []) if video is not None else 0.0
                t_res = self.text_pipeline.score_transcript(text) if text is not None else {"risk_score": 0.0}
                
                # 2. Fuse & Dispatch
                risk_data = self.aggregator.fuse(a_score, v_score, t_res["risk_score"])
                self.dispatcher.dispatch(risk_data)
                
            await asyncio.sleep(0.01) # Prevent CPU pinning

    async def run(self):
        await asyncio.gather(self.worker_loop())

if __name__ == "__main__":
    router = StreamRouter()
    loop = asyncio.get_event_loop()
    # Mock ingestion
    async def mock_call():
        await router.ingest_audio(np.random.randn(32000))
        await router.ingest_text("I am your son, send money now!")
        await asyncio.sleep(1)
    
    loop.run_until_complete(asyncio.gather(router.run(), mock_call()))
