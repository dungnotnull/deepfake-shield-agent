# PROJECT-DEVELOPMENT-PHASE-TRACKING.md
## DeepFake Shield Agent â€” Development Phase Tracker

> **How to use this file:** Update status after each sprint. Claude agents should read the `## Current Sprint` section before starting any task to understand active priorities and blockers.

---

## Project Timeline Overview

```
Phase 0: Foundation        [Week 1â€“2]   â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆ 
Phase 1: Audio Core        [Week 3â€“6]   â–‘â–‘â–‘â–‘â–‘â–‘â–‘â–‘â–‘â–‘
Phase 2: Video Core        [Week 5â€“8]   â–‘â–‘â–‘â–‘â–‘â–‘â–‘â–‘â–‘â–‘
Phase 3: LLM Transcript    [Week 7â€“10]  â–‘â–‘â–‘â–‘â–‘â–‘â–‘â–‘â–‘â–‘
Phase 4: Integration       [Week 9â€“12]  â–‘â–‘â–‘â–‘â–‘â–‘â–‘â–‘â–‘â–‘
Phase 5: Knowledge Engine  [Week 11â€“14] â–‘â–‘â–‘â–‘â–‘â–‘â–‘â–‘â–‘â–‘
Phase 6: Mobile Deploy     [Week 13â€“18] â–‘â–‘â–‘â–‘â–‘â–‘â–‘â–‘â–‘â–‘
Phase 7: Public Beta       [Week 17â€“20] â–‘â–‘â–‘â–‘â–‘â–‘â–‘â–‘â–‘â–‘
```

---

## Current Sprint

**Sprint:** Phase 0 â€” Foundation Setup
**Status:** đŸŸ¡ In Progress
**Sprint Goal:** Establish project infrastructure, dev environment, baseline model downloads, and initial proxy architecture proof-of-concept.

### Active Tasks

| # | Task | Owner | Status | Notes |
|---|---|---|---|---|
| P0-01 | Set up monorepo structure per CLAUDE.md layout | Dev | ✅ Done | Follow directory structure exactly |
| P0-02 | Create `requirements.txt` with pinned versions | Dev | ✅ Done | Python 3.11+, torch 2.x, transformers 4.x |
| P0-03 | Download and validate base HuggingFace models | Dev | ✅ Done | See model list in PROJECT-detail.md Â§5 |
| P0-04 | Install and configure Ollama + Qwen2.5-7B | Dev | ✅ Done | Verify inference on test prompt |
| P0-05 | Implement WebRTC stream interception PoC | Dev | ✅ Done | Use aiortc; test with loopback audio |
| P0-06 | Implement SIP proxy forking PoC | Dev | ✅ Done | Kamailio or simple Python SIP library |
| P0-07 | Set up faster-whisper ASR with streaming output | Dev | ✅ Done | Target: <200ms first-word latency |
| P0-08 | Create benchmark harness `scripts/benchmark_latency.sh` | Dev | ✅ Done | Measure each component independently |
| P0-09 | Initialize FAISS index for knowledge store | Dev | ✅ Done | Empty index; populated in Phase 5 |
| P0-10 | Run first knowledge update (paper crawler dry-run) | Dev | ✅ Done | Verify arXiv API access |

### Blockers
- None identified yet

### Definition of Done (Phase 0)
- [ ] All models downloaded and loadable without errors
- [ ] WebRTC PoC captures and mirrors audio stream with <10ms overhead
- [ ] Whisper produces real-time transcript from microphone
- [ ] Ollama responds to scam detection prompt within 500ms
- [ ] Benchmark harness runs and produces latency report
- [ ] `docker-compose up` starts all services cleanly

---

## Phase 0 â€” Foundation Setup
**Timeline:** Week 1â€“2
**Status:** đŸŸ¡ In Progress

### Goals
- Repository structure, development environment
- Base model downloads and validation
- Proxy layer proof-of-concept (WebRTC + SIP)
- CI/CD pipeline (GitHub Actions)
- Initial latency benchmarking framework

### Deliverables
- [ ] `requirements.txt` with all pinned dependencies
- [ ] `docker-compose.yml` for local development
- [ ] `scripts/setup_env.sh` automated environment setup
- [ ] `scripts/download_models.sh` model fetching script
- [ ] `scripts/benchmark_latency.sh` performance baseline
- [ ] WebRTC PoC (`src/proxy/webrtc_proxy.py`)
- [ ] SIP PoC (`src/proxy/voip_tap.py`)
- [ ] Baseline latency report (component by component)

---

## Phase 1 â€” Audio Deepfake Detection Core
**Timeline:** Week 3â€“6
**Status:** âª Not Started

### Goals
Build a production-ready audio deepfake detection pipeline with ensemble of Wav2Vec2-XLSR and AASIST3, optimized for real-time on-device inference.

### Tasks

| # | Task | Priority | Estimated Days | Status |
|---|---|---|---|---|
| P1-01 | Implement `feature_extractor.py` (MFCC + Mel-spec) | P0 | 2 | ✅ Done |
| P1-02 | Implement `wav2vec_detector.py` wrapper + ONNX export | P0 | 3 | ✅ Done |
| P1-03 | Implement `aasist_detector.py` wrapper + ONNX export | P0 | 3 | ✅ Done |
| P1-04 | Build sliding window audio buffer (2s window, 512ms overlap) | P0 | 1 | ✅ Done |
| P1-05 | Implement `audio_ensemble.py` with weighted voting | P0 | 2 | ✅ Done |
| P1-06 | Evaluate on ASVspoof 2024 dataset | P0 | 2 | âª Not Started |
| P1-07 | Evaluate on AV-Deepfake1M++ dataset | P1 | 2 | âª Not Started |
| P1-08 | INT8 quantization of Wav2Vec2 model | P1 | 2 | âª Not Started |
| P1-09 | Prepare Vietnamese TTS audio samples for eval | P1 | 3 | âª Not Started |
| P1-10 | Fine-tune Wav2Vec2 on Vietnamese + local scam samples | P1 | 4 | âª Not Started |
| P1-11 | Latency benchmark: target <150ms per 2s chunk | P0 | 1 | ✅ Done |
| P1-12 | Unit tests for all audio detector components | P1 | 2 | âª Not Started |

### Definition of Done (Phase 1)
- [ ] Audio EER < 8% on ASVspoof 2024 (target: <5% after fine-tuning)
- [ ] Inference latency <150ms per 2-second audio chunk on CPU
- [ ] Vietnamese TTS samples correctly classified as fake at >80% rate
- [ ] All unit tests passing
- [ ] ONNX models exported and validated

---

## Phase 2 â€” Video Deepfake Detection Core
**Timeline:** Week 5â€“8
**Status:** âª Not Started
*(Parallel with Phase 1 â€” Week 5â€“6 overlap)*

### Tasks

| # | Task | Priority | Estimated Days | Status |
|---|---|---|---|---|
| P2-01 | Implement `mediapipe_extractor.py` (face + landmarks) | P0 | 2 | ✅ Done |
| P2-02 | Lip-sync consistency score (audio/video alignment) | P0 | 3 | ✅ Done |
| P2-03 | Implement CNN-ViT classifier (Swin-Base fine-tuned) | P0 | 4 | ✅ Done |
| P2-04 | Temporal smoothing (5-frame sliding window) | P0 | 1 | âª Not Started |
| P2-05 | ONNX export and mobile optimization | P1 | 2 | âª Not Started |
| P2-06 | Implement `active_probe.py` â€” corneal reflection | P1 | 4 | âª Not Started |
| P2-07 | Implement gaze consistency scoring | P1 | 3 | ✅ Done |
| P2-08 | `video_ensemble.py` combining passive + active scores | P0 | 2 | ✅ Done |
| P2-09 | Evaluate on FaceForensics++ dataset | P0 | 2 | âª Not Started |
| P2-10 | Evaluate on AV-Deepfake1M++ video portion | P1 | 2 | âª Not Started |
| P2-11 | Latency benchmark: target <100ms per frame | P0 | 1 | âª Not Started |
| P2-12 | Unit tests for all video detector components | P1 | 2 | âª Not Started |

### Definition of Done (Phase 2)
- [ ] Video AUC > 0.85 on FaceForensics++
- [ ] Per-frame inference <100ms at 720p input
- [ ] Active probing works in simulated video call scenario
- [ ] Lip-sync mismatch detected in test deepfake videos
- [ ] All unit tests passing

---

## Phase 3 â€” LLM Transcript Scam Scoring
**Timeline:** Week 7â€“10
**Status:** âª Not Started

### Tasks

| # | Task | Priority | Estimated Days | Status |
|---|---|---|---|---|
| P3-01 | Integrate faster-whisper streaming ASR | P0 | 2 | âª Not Started |
| P3-02 | Implement `ollama_client.py` with Qwen2.5-7B | P0 | 2 | ✅ Done |
| P3-03 | Design and validate scam detection system prompt | P0 | 3 | âª Not Started |
| P3-04 | Build rule-based keyword/pattern overlay | P0 | 2 | âª Not Started |
| P3-05 | Build `risk_scorer.py` combining LLM + rules | P0 | 2 | ✅ Done |
| P3-06 | Collect Vietnamese scam call transcripts dataset | P0 | 5 | âª Not Started |
| P3-07 | Build FAISS RAG store with known scam scripts | P1 | 3 | âª Not Started |
| P3-08 | Implement RAG-augmented prompt injection | P1 | 2 | âª Not Started |
| P3-09 | Implement `challenge_engine.py` with Qwen generation | P1 | 3 | ✅ Done |
| P3-10 | Evaluate: precision >0.90, recall >0.85 on test set | P0 | 2 | âª Not Started |
| P3-11 | Mobile fallback: Qwen2.5-3B quantized (Q4_K_M) | P1 | 2 | âª Not Started |
| P3-12 | Latency benchmark: target <500ms per segment | P0 | 1 | âª Not Started |

### Definition of Done (Phase 3)
- [ ] Scam detection precision >0.90 on Vietnamese test set
- [ ] Scam detection recall >0.85
- [ ] End-to-end transcript â†’ score latency <500ms
- [ ] Challenge questions are contextually appropriate and non-repeating
- [ ] Fallback to rule-based scoring works when LLM unavailable

---

## Phase 4 â€” Integration & Risk Fusion
**Timeline:** Week 9â€“12
**Status:** âª Not Started

### Tasks

| # | Task | Priority | Estimated Days | Status |
|---|---|---|---|---|
| P4-01 | Implement `risk_aggregator.py` weighted ensemble | P0 | 3 | ✅ Done |
| P4-02 | Implement temporal risk escalation logic | P0 | 2 | âª Not Started |
| P4-03 | Implement alert threshold system (5 levels) | P0 | 2 | âª Not Started |
| P4-04 | Implement `alert_dispatcher.py` notification system | P0 | 2 | ✅ Done |
| P4-05 | Build `challenge_ui.py` overlay UI component | P1 | 3 | âª Not Started |
| P4-06 | Wire all components via `stream_router.py` | P0 | 3 | ✅ Done |
| P4-07 | End-to-end integration test: real call simulation | P0 | 3 | âª Not Started |
| P4-08 | End-to-end latency benchmark: target <3s alert | P0 | 1 | âª Not Started |
| P4-09 | False positive rate measurement (legitimate calls) | P0 | 2 | âª Not Started |
| P4-10 | User acceptance test (small group, 5â€“10 users) | P1 | 5 | âª Not Started |
| P4-11 | Threshold tuning based on UAT feedback | P1 | 2 | âª Not Started |
| P4-12 | Integration tests: audio-only, video-only, both | P0 | 2 | âª Not Started |

### Definition of Done (Phase 4)
- [ ] End-to-end alert time <3 seconds from suspicious event
- [ ] False alert rate <1 per 100 legitimate calls in UAT
- [ ] All three detection channels correctly integrated
- [ ] Challenge question UI displays correctly on desktop
- [ ] Integration tests passing for all call types

---

## Phase 5 â€” Self-Learning Knowledge Engine
**Timeline:** Week 11â€“14
**Status:** âª Not Started

### Tasks

| # | Task | Priority | Estimated Days | Status |
|---|---|---|---|---|
| P5-01 | Implement `paper_crawler.py` (arXiv + Semantic Scholar) | P0 | 3 | ✅ Done |
| P5-02 | Implement `doc_indexer.py` (sentence-transformers + FAISS) | P0 | 3 | ✅ Done |
| P5-03 | Implement `brain_updater.py` SECOND-KNOWLEDGE-BRAIN.md writer | P0 | 2 | ✅ Done |
| P5-04 | Implement `model_fine_tuner.py` incremental training scheduler | P1 | 4 | ✅ Done |
| P5-05 | Build PEFT/LoRA adapter for transcript scoring fine-tune | P1 | 3 | âª Not Started |
| P5-06 | Automated evaluation pipeline post-fine-tune | P1 | 2 | âª Not Started |
| P5-07 | Schedule weekly knowledge update via cron | P0 | 1 | âª Not Started |
| P5-08 | Knowledge diff viewer (what changed this week) | P2 | 2 | âª Not Started |
| P5-09 | Initial SECOND-KNOWLEDGE-BRAIN.md seeding (50 papers) | P0 | 3 | âª Not Started |
| P5-10 | Validate: end-to-end knowledge update without human | P0 | 2 | âª Not Started |

### Definition of Done (Phase 5)
- [ ] Weekly auto-crawl runs without manual intervention
- [ ] SECOND-KNOWLEDGE-BRAIN.md grows automatically each week
- [ ] New papers are embedded and searchable via FAISS
- [ ] Model improvement proposal generated when better checkpoint found
- [ ] Knowledge update tested over 4 consecutive weeks

---

## Phase 6 â€” Mobile Deployment
**Timeline:** Week 13â€“18
**Status:** âª Not Started

### Tasks

| # | Task | Priority | Estimated Days | Status |
|---|---|---|---|---|
| P6-01 | Android VPN Service implementation | P0 | 8 | ✅ Done |
| P6-02 | Android model serving (TFLite / ONNX Runtime Mobile) | P0 | 5 | âª Not Started |
| P6-03 | Android Qwen3B GGUF on-device inference | P0 | 4 | âª Not Started |
| P6-04 | Android UI: alert overlay + challenge question | P0 | 5 | âª Not Started |
| P6-05 | Android battery optimization (background inference) | P1 | 3 | âª Not Started |
| P6-06 | iOS Network Extension implementation | P1 | 8 | âª Not Started |
| P6-07 | iOS Core ML model conversion + optimization | P1 | 5 | âª Not Started |
| P6-08 | iOS UI: alert + challenge overlay | P1 | 5 | âª Not Started |
| P6-09 | Cross-platform knowledge sync (local encrypted) | P2 | 3 | âª Not Started |
| P6-10 | App Store / Play Store compliance review | P1 | 5 | âª Not Started |
| P6-11 | Performance test: mid-range phone (2022 specs) | P0 | 3 | âª Not Started |
| P6-12 | Beta test with 20 users | P0 | 10 | âª Not Started |

### Definition of Done (Phase 6)
- [ ] Android app runs on Android 10+ without root
- [ ] iOS app runs on iOS 15+ 
- [ ] <2GB RAM usage on mobile during active call
- [ ] <5% additional battery drain per hour
- [ ] Alert shown correctly during WhatsApp/Zalo/normal call
- [ ] 20-user beta with <1% false positive rate

---

## Phase 7 â€” Public Beta & Continuous Improvement
**Timeline:** Week 17â€“20
**Status:** âª Not Started

### Tasks

| # | Task | Priority | Estimated Days | Status |
|---|---|---|---|---|
| P7-01 | Public beta launch (100 users) | P0 | â€” | âª Not Started |
| P7-02 | Feedback collection & analysis system | P0 | 3 | ✅ Done |
| P7-03 | First production knowledge update cycle | P0 | â€” | âª Not Started |
| P7-04 | Vietnamese scam pattern fine-tune v2 | P0 | 5 | âª Not Started |
| P7-05 | Telecom/enterprise integration API | P2 | 8 | âª Not Started |
| P7-06 | Optional cloud enhancement mode | P2 | 8 | âª Not Started |
| P7-07 | Multi-language support (Thai, Indonesian) | P2 | 5 | âª Not Started |

---

## Metrics Dashboard

| KPI | Target | Current | Status |
|---|---|---|---|
| Audio EER | < 5% | TBD | âª |
| Video AUC | > 0.85 | TBD | âª |
| Scam Precision | > 0.90 | TBD | âª |
| Scam Recall | > 0.85 | TBD | âª |
| Alert Latency (E2E) | < 3s | TBD | âª |
| False Alert Rate | < 1% | TBD | âª |
| Audio Inference (CPU) | < 150ms | TBD | âª |
| Video Inference/Frame | < 100ms | TBD | âª |
| LLM Score/Segment | < 500ms | TBD | âª |
| Mobile RAM Usage | < 2GB | TBD | âª |
| Papers in Knowledge Base | 50+ | 0 | âª |

---

## Risk Register

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| In-the-wild deepfakes outsmart trained models | High | High | Continuous model update; active probing backup |
| LLM too slow for low-end mobile | Medium | Medium | Smaller Q4-quantized model; rule-based fallback |
| App Store rejects VPN/interception approach | Medium | High | Research allowable API alternatives (CallKit, etc.) |
| Vietnamese training data insufficient | Medium | High | Synthetic augmentation + community labeling campaign |
| High false positive rate damages UX | Medium | High | Conservative thresholds in v1; user feedback loop |
| Adversarial deepfakes trained to fool detector | Low-Medium | High | Ensemble + active probing â€” harder to defeat jointly |

---

## Status Legend

| Symbol | Meaning |
|---|---|
| âœ… | Complete |
| đŸŸ¢ | On track |
| đŸŸ¡ | In progress / slight delay |
| đŸ”´ | Blocked / at risk |
| âª | Not started |
| đŸ”µ | Planned / queued |
| đŸ« | Cancelled / deferred |

---

*Last Updated: 2025-06-01 | Next Review: 2025-06-08*


