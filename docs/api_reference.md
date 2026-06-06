# API Reference: DeepFake Shield Agent

## Internal Event Flow
`Proxy Layer` -> `StreamRouter` -> `[AudioDet, VideoDet, TextDet]` -> `RiskAggregator` -> `AlertDispatcher`

## Enterprise API (FastAPI)
### POST /analyze
- **Input**: JSON { call_id, audio_chunk, video_frame, transcript }
- **Output**: JSON { risk_level, score, recommendation }
