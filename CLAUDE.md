# CLAUDE.md — DeepFake Shield Agent

> **Operational handbook for AI agents, Claude Code, and contributors.**
> This file tells any Claude instance (or developer) everything it needs to understand, build, and extend this project without prior context.

---

## 1. Project Identity

| Field | Value |
|---|---|
| **Project Name** | deepfake-shield-agent |
| **Codename** | Shield |
| **Mission** | Real-time deepfake detection and fraud warning system for voice/video calls |
| **Primary Threat** | AI-generated voice cloning & face-swap impersonation used in financial scams |
| **Target Users** | Individuals (especially elderly), enterprises, banks, telecom operators |
| **Privacy Posture** | Privacy-first: all inference runs on-device; no audio/video leaves the device |

---

## 2. Repository Layout

```
deepfake-shield-agent/
├── CLAUDE.md                          ← You are here (agent operational guide)
├── PROJECT-detail.md                  ← Full architecture & technical spec
├── PROJECT-DEVELOPMENT-PHASE-TRACKING.md ← Sprint & milestone tracker
├── SECOND-KNOWLEDGE-BRAIN.md         ← Living research knowledge base
│
├── src/
│   ├── proxy/                         ← WebRTC/VoIP interception layer
│   │   ├── webrtc_proxy.py
│   │   ├── voip_tap.py
│   │   └── stream_router.py
│   │
│   ├── audio_detector/                ← Audio deepfake detection pipeline
│   │   ├── feature_extractor.py       ← MFCC / Mel-spectrogram / raw waveform
│   │   ├── wav2vec_detector.py        ← Wav2Vec2 fine-tuned classifier
│   │   ├── aasist_detector.py         ← AASIST / AASIST3 model wrapper
│   │   └── audio_ensemble.py          ← Ensemble voting logic
│   │
│   ├── video_detector/                ← Visual deepfake detection pipeline
│   │   ├── mediapipe_extractor.py     ← Landmark + lip-sync extraction
│   │   ├── cnn_vit_detector.py        ← Hybrid CNN+ViT face forgery detector
│   │   ├── active_probe.py            ← Corneal-reflection / gaze active probe
│   │   └── video_ensemble.py
│   │
│   ├── transcript_agent/              ← LLM-based scam scoring
│   │   ├── asr_engine.py              ← Whisper / faster-whisper ASR
│   │   ├── ollama_client.py           ← Local Qwen/Llama inference via Ollama
│   │   ├── risk_scorer.py             ← Rule + LLM hybrid risk scoring
│   │   └── challenge_engine.py        ← Security challenge question generator
│   │
│   ├── knowledge_updater/             ← Self-learning knowledge pipeline
│   │   ├── paper_crawler.py           ← arXiv / Semantic Scholar crawler
│   │   ├── doc_indexer.py             ← Embedding & FAISS indexer
│   │   ├── brain_updater.py           ← Writes to SECOND-KNOWLEDGE-BRAIN.md
│   │   └── model_fine_tuner.py        ← Incremental fine-tuning scheduler
│   │
│   ├── alert_engine/                  ← Risk aggregation & notification
│   │   ├── risk_aggregator.py         ← Multi-modal score fusion
│   │   ├── alert_dispatcher.py        ← UI/notification push
│   │   └── challenge_ui.py            ← Challenge question overlay UI
│   │
│   └── utils/
│       ├── config.py
│       ├── logger.py
│       └── device_optimizer.py        ← ONNX / TFLite export helpers
│
├── models/
│   ├── audio/                         ← Pretrained & fine-tuned audio models
│   ├── video/                         ← Pretrained & fine-tuned video models
│   └── llm/                           ← Ollama model configs
│
├── data/
│   ├── datasets/                      ← ASVspoof, FaceForensics++, AV-Deepfake1M
│   └── fine_tune/                     ← Local fine-tuning datasets
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
│
├── scripts/
│   ├── setup_env.sh
│   ├── download_models.sh
│   ├── run_knowledge_update.sh
│   └── benchmark_latency.sh
│
├── docs/
│   ├── architecture.md
│   ├── threat_model.md
│   └── api_reference.md
│
├── requirements.txt
├── pyproject.toml
└── docker-compose.yml
```

---

## 3. Core Agent Responsibilities

When operating as a **Claude Code** or agentic instance on this project, the agent must:

### 3.1 Build & Maintenance Tasks
- Follow `PROJECT-DEVELOPMENT-PHASE-TRACKING.md` for current sprint goals
- Never break the <200ms end-to-end latency budget for audio/video inference
- All new ML models must first be sourced from HuggingFace Hub before custom training
- Privacy rule: zero data egress — all audio/video processing is local-only

### 3.2 Knowledge Update Loop (Autonomous)
When triggered via `scripts/run_knowledge_update.sh` or scheduled cron:
1. Run `src/knowledge_updater/paper_crawler.py` to fetch latest papers
2. Summarize and embed new findings via `src/knowledge_updater/doc_indexer.py`
3. Append structured entries to `SECOND-KNOWLEDGE-BRAIN.md`
4. Evaluate if new model checkpoints outperform current production models
5. Schedule incremental fine-tuning if delta accuracy > 2% on held-out eval set
6. Commit knowledge updates with message: `chore(brain): update knowledge YYYY-MM-DD`

### 3.3 Model Selection Hierarchy (MUST follow)
```
Priority 1: Pre-trained HuggingFace models (fine-tune if needed)
Priority 2: Off-the-shelf ML algorithms (sklearn, lightgbm, etc.)
Priority 3: Custom architecture (only if Priorities 1-2 are insufficient)
```

### 3.4 Code Quality Gates
- All inference functions must have latency benchmarks in docstrings
- Every detection module must expose a `detect(stream_chunk) -> DetectionResult` interface
- Tests must cover: real audio (human), fake audio (TTS), edge cases (noisy, codec-compressed)

---

## 4. Technology Stack

| Layer | Technology | Justification |
|---|---|---|
| Audio Deepfake Detection | Wav2Vec2-XLSR + AASIST3 (HuggingFace) | State-of-art on ASVspoof benchmarks; fine-tunable |
| Video Deepfake Detection | MediaPipe + CNN-ViT hybrid | Lightweight landmark extraction + transformer accuracy |
| Active Anti-Spoofing | Corneal reflection / gaze consistency probing | Novel method, harder to defeat |
| ASR (Speech-to-Text) | faster-whisper (CTranslate2) | Low-latency, on-device, multilingual |
| Scam Transcript Analysis | Qwen-2.5-7B via Ollama | Local LLM, excellent reasoning, Vietnamese + multilingual |
| Feature Extraction | MFCC, Mel-spectrogram, Wav2Vec2 features | Proven features for audio classification |
| Model Serving | ONNX Runtime + TFLite | Cross-platform on-device inference |
| Proxy Layer | WebRTC (aiortc) + VoIP SIP proxy | Real-time stream interception |
| Knowledge Store | FAISS + MarkDown brain file | Local semantic search |
| Fine-tuning | HuggingFace Trainer + PEFT/LoRA | Efficient incremental learning |

---

## 5. Key Constraints & Non-Negotiables

```yaml
latency_budget:
  audio_detection: < 150ms per 2-second chunk
  video_detection: < 100ms per frame  
  llm_scoring: < 500ms per transcript segment (streamed)
  total_e2e_alert: < 3 seconds from suspicious event to user notification

privacy:
  audio_data: local only, no cloud
  video_data: local only, no cloud
  transcripts: local only, configurable retention (default: session-only)

accuracy_minimums:
  audio_eer: < 5% (Equal Error Rate on held-out set)
  video_auc: > 0.85
  scam_detection_precision: > 0.90 (low false-positive rate critical for UX)

supported_platforms:
  - Android (primary)
  - iOS
  - Desktop (Windows/macOS/Linux)
  - Browser extension (WebRTC)
```

---

## 6. Key Research References

See `SECOND-KNOWLEDGE-BRAIN.md` for the full living knowledge base. Core references to internalize:

- **Audio**: ASVspoof 2024 challenge baselines; AASIST/AASIST3; Wav2Vec2 fine-tuning for anti-spoofing
- **Video**: CNN-ViT hybrid for WebRTC (111–127ms latency demonstrated); Active probing via corneal reflection
- **Scam Detection**: "It Warned Me Just at the Right Moment" (LLM real-time scam detection, 2025); SAFE-QAQ framework
- **Generalization problem**: Deepfake-Eval-2024 shows 50% AUC drop on in-the-wild data — models must be continuously updated

---

## 7. Environment Setup

```bash
# Clone and setup
git clone <repo_url>
cd deepfake-shield-agent

# Install dependencies
pip install -r requirements.txt

# Download base models
bash scripts/download_models.sh

# Start Ollama with Qwen
ollama pull qwen2.5:7b

# Run initial knowledge update
bash scripts/run_knowledge_update.sh

# Start the proxy daemon
python src/proxy/webrtc_proxy.py --config config/default.yaml
```

---

## 8. Testing Commands

```bash
# Run all tests
pytest tests/ -v

# Latency benchmark
bash scripts/benchmark_latency.sh

# Simulate a scam call
python tests/e2e/simulate_scam_call.py --audio samples/scam_voice.wav --video samples/deepfake_face.mp4

# Knowledge update dry-run
python src/knowledge_updater/paper_crawler.py --dry-run --query "deepfake detection 2025"
```

---

## 9. Contributing Guidelines for Claude Agents

When writing code for this project:
1. **Always check `SECOND-KNOWLEDGE-BRAIN.md`** before implementing a detection algorithm — the latest paper may suggest a better approach
2. **Prefer ONNX export** for any model that will run on mobile
3. **Log all detection events** with timestamps and confidence scores (never raw audio/video)
4. **Challenge questions** (section 3.1) must be context-aware and unpredictable — regenerated each session
5. When in doubt about a model choice, **benchmark first** with `scripts/benchmark_latency.sh`

---

*Last updated: auto-managed by `brain_updater.py`*
