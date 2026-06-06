# PROJECT-detail.md — DeepFake Shield Agent
## Full Technical Specification & Architecture

---

## 1. Executive Summary

**DeepFake Shield Agent** is a privacy-first, real-time deepfake detection and scam prevention system designed to protect users during live voice and video calls. It operates as a transparent proxy layer that intercepts call streams, performs on-device AI analysis across three independent detection channels (audio biometrics, visual forgery, and linguistic scam patterns), and triggers immediate protective actions when a threat is detected.

**The core insight:** Deepfake scammers typically deploy a combination of voice cloning (to impersonate a family member) and face-swap technology (in video calls) while using scripted pressure tactics to demand money. Catching any one of these three signals is sufficient for an early warning; catching multiple signals triggers a hard alert.

---

## 2. Threat Model

### 2.1 Primary Attack Vectors

| Attack | Description | Frequency |
|---|---|---|
| Voice Cloning Scam | Clone a family member's voice with 3–10 seconds of sample audio; call elderly target requesting emergency money transfer | Very High (primary threat) |
| Face-Swap Video Call | Real-time face-swap impersonating family/authority figures via Zoom/WhatsApp video calls | Growing rapidly (2024–2025) |
| AI-Scripted Pressure | LLM-generated urgent scripts ("I'm in jail, send bail money NOW") designed to bypass rational thinking | Emerging |
| Hybrid Attack | All three combined for maximum credibility | Highest severity |

### 2.2 Out of Scope (v1.0)
- Text-based phishing (separate product)
- Pre-recorded video deepfakes (addressed in v2.0)
- Network-layer caller ID spoofing (carrier-side problem)

---

## 3. System Architecture

### 3.1 High-Level Data Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                        CALL STREAM                               │
│         (WebRTC / VoIP SIP / Mobile call audio)                 │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                    ┌─────▼──────┐
                    │   PROXY    │  WebRTC/VoIP transparent tap
                    │   LAYER    │  (aiortc / SIP proxy)
                    └──┬──┬──┬───┘
                       │  │  │
          ┌────────────┘  │  └─────────────┐
          │               │                │
    ┌─────▼──────┐  ┌─────▼──────┐  ┌─────▼──────┐
    │   AUDIO    │  │   VIDEO    │  │   TEXT     │
    │ DETECTOR   │  │ DETECTOR   │  │  AGENT     │
    │            │  │            │  │ (LLM+RAG)  │
    │ Wav2Vec2   │  │ MediaPipe  │  │            │
    │ + AASIST3  │  │ + CNN-ViT  │  │ Whisper    │
    │            │  │ + Active   │  │ → Qwen 7B  │
    │            │  │  Probe     │  │ via Ollama │
    └─────┬──────┘  └─────┬──────┘  └─────┬──────┘
          │               │                │
          └───────────────┼────────────────┘
                          │
                  ┌───────▼────────┐
                  │  RISK FUSION   │  Weighted ensemble
                  │   ENGINE       │  + temporal context
                  └───────┬────────┘
                          │
               ┌──────────┼──────────┐
               │          │          │
         ┌─────▼─────┐ ┌──▼───┐ ┌───▼──────────┐
         │  NORMAL   │ │WARN  │ │   ALERT +    │
         │ CONTINUE  │ │ USER │ │  CHALLENGE   │
         └───────────┘ └──────┘ └──────────────┘
```

### 3.2 Component Architecture Detail

#### Layer 1: Proxy Interception

The proxy layer operates as a transparent man-in-the-middle on the local device only. No traffic is re-routed off-device.

**For mobile (Android/iOS):**
- Register as a `VpnService` (Android) or `Network Extension` (iOS)
- Intercept RTP/RTSP packets from calling apps
- Forward unmodified to the actual destination (zero latency impact on the call itself)
- Mirror a copy of the stream to the detection pipeline

**For WebRTC (browser/desktop):**
- Browser extension injects JavaScript into the calling page
- Hooks into `MediaStream` and `RTCPeerConnection` APIs
- Clones audio/video tracks to the local WASM-based detection worker

**For VoIP/SIP:**
- Local SIP proxy (Kamailio or equivalent) configured as a forking proxy
- Forks one leg of the call to the detection pipeline
- Operates transparently on the `127.0.0.1` loopback interface

#### Layer 2: Audio Deepfake Detection

**Pipeline:**
```
Raw PCM audio (16kHz, mono)
  → 2-second sliding window (512ms overlap)
  → Feature extraction (MFCC 80-dim + Mel-spectrogram 128-bin)
  → Wav2Vec2-XLSR encoder (frozen base + fine-tuned classifier head)
  → AASIST3 graph attention network (parallel inference)
  → Ensemble vote (weighted average)
  → Probability score: P(fake) ∈ [0.0, 1.0]
```

**Models (HuggingFace):**
- Base: `Gustking/wav2vec2-large-xlsr-deepfake-audio-classification`
- Enhanced: `lab260/AASIST3` (Wav2Vec2 + KAN + GAT architecture)
- Fine-tuning dataset: ASVspoof 2024 + AV-Deepfake1M++ + custom collected samples
- Target: EER < 5% on held-out set

**Optimization for on-device:**
- Export to ONNX with INT8 quantization → ~40% size reduction
- Use CTranslate2 for transformer inference acceleration
- Target: <150ms per 2-second audio chunk on mid-range mobile

**Additional audio signals analyzed:**
- Unnatural phoneme transitions (stitching artifacts from TTS)
- Missing background noise correlation between speakers (clone typically lacks ambient noise)
- Spectral inconsistencies in high-frequency range (>8kHz) typical of vocoders
- Prosody anomalies: robotic rhythm, unnaturally flat emotion

#### Layer 3: Video Deepfake Detection

**Pipeline:**
```
Video frame (30fps, 720p downsampled to 224x224)
  → Face detection (MediaPipe BlazeFace, ~1ms/frame)
  → 68-point facial landmark extraction (MediaPipe FaceMesh)
  → Lip-sync consistency check (audio-visual alignment score)
  → CNN-ViT hybrid feature extraction (EfficientNet-B4 + ViT-Base)
  → ONNX inference → P(fake) per frame
  → Temporal smoothing (5-frame sliding window median)
```

**Active Probing (Anti-Spoofing):**
Two novel approaches that are difficult for real-time deepfakes to defeat:

1. **Corneal Reflection Probe**: Display a known pattern (brief flash or static image) on screen during a shared screen moment; analyze corneal reflections in the opponent's eye for consistency. Implemented from Guo et al. (2022).

2. **Gaze Consistency Probe**: Real-time deepfakes cannot perfectly replicate natural gaze behavior during conversation. Track point-of-gaze patterns and compare against normal conversational distributions. Implemented from gaze tracking research (2025).

3. **Micro-expression Consistency**: Face-swapped video often introduces unnatural micro-expression timing. MediaPipe's 468 facial landmarks allow tracking of subtle muscle movements.

**Models:**
- Face detection: MediaPipe BlazeFace (WASM, <1ms)
- Deep classification: `microsoft/swin-base-patch4-window7-224` fine-tuned on FaceForensics++
- Alternative: CNN-ViT hybrid from Springer 2026 paper (98.33% accuracy, 111–127ms E2E)

#### Layer 4: Transcript Scam Scoring (LLM Agent)

**Pipeline:**
```
Audio stream
  → faster-whisper (CTranslate2) ASR → rolling transcript (5-second lag)
  → Sentence chunking (semantic boundaries)
  → Ollama: Qwen2.5-7B local inference
  → Prompt: scam pattern classification + risk score 0-100
  → Rule engine overlay (keyword triggers, pressure pattern detection)
  → Risk delta tracking over conversation duration
```

**Qwen System Prompt (core):**
```
You are a real-time scam detection assistant. Analyze the following phone call transcript 
segment and return a JSON object with:
- risk_score: 0-100 (100 = confirmed scam)
- detected_patterns: list of identified scam signals
- reasoning: brief explanation (max 2 sentences)
- recommended_action: "none" | "warn" | "challenge" | "block"

Scam signals to detect:
- Urgency/emergency pressure ("I'm in jail", "accident happened")
- Money transfer requests (any method: bank, crypto, gift cards)
- Identity claims that cannot be verified
- Isolation tactics ("don't tell anyone", "police will come")
- Authority impersonation (police, bank, government)
- Emotional manipulation targeting elderly
- Requests for OTP/verification codes
```

**Why local LLM instead of cloud:**
- Vietnamese scam scripts not well-represented in cloud APIs
- Zero latency from network round-trips
- No privacy exposure of call content
- Works offline and in poor connectivity areas
- Continuously fine-tunable on locally collected scam transcripts

**RAG Integration:**
- FAISS vector store of known scam scripts (local)
- Augments LLM prompt with similar past scam patterns
- Updated automatically as new scam variants are discovered

#### Layer 5: Risk Fusion Engine

**Weighted ensemble scoring:**
```python
# Risk weights (empirically tuned, adjustable via config)
WEIGHTS = {
    "audio_deepfake": 0.35,      # High weight - voice clone is primary attack
    "video_deepfake": 0.30,      # High weight for video calls
    "scam_transcript": 0.35,     # Equal weight - linguistic patterns are reliable
}

def fuse_risk(audio_score, video_score, transcript_score, call_type):
    if call_type == "audio_only":
        # Redistribute video weight
        adjusted = {
            "audio_deepfake": 0.55,
            "scam_transcript": 0.45,
        }
    composite = weighted_sum(scores, adjusted)
    
    # Hard override: any single modality >= 0.90 → immediate alert
    if max(audio_score, video_score, transcript_score) >= 0.90:
        return AlertLevel.CRITICAL
    
    # Temporal escalation: rising score over 30 seconds
    if trend_is_rising(history) and composite > 0.60:
        return AlertLevel.WARNING
    
    return threshold_to_level(composite)
```

**Alert Levels:**
| Level | Condition | Action |
|---|---|---|
| NORMAL | Composite < 0.40 | Silent, continue monitoring |
| CAUTION | 0.40–0.60 | Subtle UI indicator, no interruption |
| WARNING | 0.60–0.80 | Overlay warning banner, offer to pause call |
| ALERT | 0.80–0.90 | Interrupt call, show warning + challenge options |
| CRITICAL | > 0.90 or hard trigger | Pause call, mandatory challenge question |

#### Layer 6: Challenge Question Engine

When ALERT or CRITICAL is triggered, the system generates a context-aware security challenge:

```
Challenge types (randomly selected, context-aware):
1. Personal Memory Challenge: "Ask them: what did we eat at your birthday dinner last year?"
2. Shared Secret Challenge: "Ask them: what's the nickname only you two know?"
3. Knowledge Challenge: "Ask them: what street did Grandma grow up on?"
4. Real-time Verification: "Ask them to wave their right hand 3 times"
5. Code Word Challenge: (if pre-configured) "Ask for your family safe word"
```

**Challenge generation uses:**
- Qwen local LLM to generate natural-language prompts
- User's pre-configured contact profile (optional family info)
- Session context from the current conversation

---

## 4. Self-Learning Knowledge Architecture

This is the key competitive differentiator: the system becomes more accurate over time.

### 4.1 Knowledge Update Pipeline

```
Scheduled (weekly) or Manual trigger
  │
  ├─ paper_crawler.py
  │    ├─ Query arXiv API: "deepfake detection", "anti-spoofing", "phone scam LLM"
  │    ├─ Query Semantic Scholar: same queries + citation depth 1
  │    ├─ Query ACL Anthology: "scam detection", "fraud NLP"
  │    └─ Filter: published after last_update, relevance_score > 0.7
  │
  ├─ doc_indexer.py
  │    ├─ Extract abstract + methods + results sections
  │    ├─ Generate embeddings via sentence-transformers/all-mpnet-base-v2
  │    └─ Store in FAISS index (./knowledge/faiss.index)
  │
  ├─ brain_updater.py
  │    ├─ Synthesize new findings into structured entries
  │    ├─ Append to SECOND-KNOWLEDGE-BRAIN.md
  │    └─ Flag entries that suggest model or prompt improvements
  │
  └─ model_fine_tuner.py
       ├─ Check if new benchmark datasets are available
       ├─ Evaluate current production models on new data
       ├─ If delta_accuracy > 2%: schedule fine-tuning job
       └─ Update model registry on successful fine-tune
```

### 4.2 Scam Pattern Learning

```
Daily pipeline:
  ├─ Collect flagged call transcripts (user-consented only)
  ├─ Semi-automatic labeling (LLM + human review for confirmed cases)
  ├─ Augment RAG store with new scam scripts
  └─ Periodic LoRA fine-tune of transcript scoring model
```

---

## 5. ML/DL Model Specifications

### 5.1 Audio Models

| Model | Source | Task | Size | Latency | Accuracy |
|---|---|---|---|---|---|
| Wav2Vec2-XLSR Deepfake | HuggingFace `Gustking/...` | Binary: real vs fake | ~300MB | ~120ms | EER ~3-5% |
| AASIST3 | HuggingFace `lab260/AASIST3` | Anti-spoofing | ~180MB | ~80ms | ASVspoof2024 SOTA |
| faster-whisper (medium) | `Systran/faster-whisper-medium` | ASR transcription | ~770MB | ~200ms (streaming) | WER <10% |
| Audio Ensemble | Custom voting layer | Combined score | N/A | +5ms | Best of both |

### 5.2 Video Models

| Model | Source | Task | Size | Latency | Accuracy |
|---|---|---|---|---|---|
| MediaPipe BlazeFace | Google | Face detection + landmarks | ~2MB | <2ms/frame | 99%+ detection |
| Swin-Base FaceForensics++ | HuggingFace fine-tuned | Face forgery | ~350MB | ~80ms | AUC 0.95+ |
| EfficientNet-B4 + ViT | Custom ensemble | Spatial + temporal | ~200MB | ~50ms | AUC 0.92+ |

### 5.3 LLM Component

| Model | Runtime | Task | Size | Latency |
|---|---|---|---|---|
| Qwen2.5-7B-Instruct | Ollama | Scam transcript scoring | ~4.7GB (Q4) | ~300–500ms |
| sentence-transformers/all-mpnet | HuggingFace | RAG embeddings | ~420MB | <50ms |
| Qwen2.5-3B-Instruct | Ollama | Mobile fallback | ~2.2GB (Q4) | ~150ms |

---

## 6. Privacy & Security Design

### 6.1 Data Minimization
- Audio/video buffers are circular, max 30 seconds retained in RAM
- No audio or video is ever written to disk during detection
- Transcripts stored in RAM only; optional user-controlled session export
- All model inference is local; no telemetry by default

### 6.2 On-Device Encryption
- Knowledge base (FAISS index + SECOND-KNOWLEDGE-BRAIN.md) encrypted at rest (AES-256)
- User profile and challenge question vault encrypted with device keychain

### 6.3 Threat to the Detector
- Adversarial audio attacks: mitigated by ensemble of two independent architectures
- Adaptive deepfakes trained to fool detectors: mitigated by active probing methods (corneal/gaze)
- Model poisoning: fine-tuning pipeline uses human review gate for confirmed cases only

---

## 7. Performance Targets & Benchmarks

### 7.1 Latency Budget (end-to-end alert from suspicious event)

```
Event detected at t=0
  ├─ Audio detector fires:     t + 150ms (2-second chunk + inference)
  ├─ Video detector fires:     t + 100ms (per frame)
  ├─ LLM scam score returns:   t + 500ms (5-second transcript chunk + inference)
  ├─ Risk fusion:              t + 510ms (+10ms aggregation)
  └─ Alert shown to user:      t + 600ms (best case), t + 3000ms (LLM-triggered)
```

### 7.2 Accuracy Targets

| Metric | Target | Measurement |
|---|---|---|
| Audio EER | < 5% | ASVspoof 2024 + in-house test set |
| Video AUC | > 0.85 | FaceForensics++ + AV-Deepfake1M |
| Scam Precision | > 0.90 | Minimize false positives (UX critical) |
| Scam Recall | > 0.85 | Catch most real scams |
| False Alert Rate | < 1 per 100 legitimate calls | UX requirement |

### 7.3 Resource Budget (mobile mid-range device)

| Resource | Budget |
|---|---|
| RAM | < 2GB total for all models + buffers |
| CPU | < 20% sustained load (background operation) |
| Battery | < 5% additional drain per hour of call |
| Storage | < 3GB for all models (compressed) |

---

## 8. Integration & Deployment Targets

### 8.1 Phase 1 — Desktop/Extension (v0.1–v0.2)
- Chrome/Firefox extension for WebRTC calls (Zoom, Google Meet, Teams, WhatsApp Web)
- Desktop daemon for desktop calling apps

### 8.2 Phase 2 — Mobile (v0.3–v0.5)
- Android VPN Service for call interception
- iOS Network Extension (App Store compliant approach)

### 8.3 Phase 3 — Telecom Integration (v0.6+)
- SIP proxy integration for VoIP providers
- Bank/enterprise API for high-risk call monitoring
- Optional cloud-based enhancement mode (consent-required, encrypted)

---

## 9. Known Limitations & Mitigations

| Limitation | Impact | Mitigation |
|---|---|---|
| Deepfake-Eval-2024 shows 50% AUC drop in-the-wild | Current models may miss novel deepfakes | Continuous knowledge update + model refresh |
| LLM latency (300–500ms) too slow for single-sentence scams | May miss very short scam triggers | Rule-based layer catches keyword triggers instantly |
| On-device RAM constraints limit model size | Cannot run largest SOTA models | Ensemble of smaller specialized models |
| Active probing requires screen interaction | Not always possible in passive calls | Falls back to passive detection only |
| Vietnamese/multilingual scam scripts under-represented | Lower accuracy for local dialects | Priority fine-tuning dataset in Vietnamese |
| Cold-start: first 10 seconds of call are unscored | Scammer may get initial hook in | Pre-call number risk check (OSINT lookup) |

---

## 10. Improvement Recommendations Over Original Concept

The following improvements were added to the original project idea:

1. **Active Probing Layer**: Original concept was passive-only. Added corneal reflection + gaze consistency probing — these are significantly harder for deepfakes to defeat and represent the current research frontier (2024–2025).

2. **Ensemble Architecture**: Original specified single models (Wav2Vec2 OR MediaPipe). Changed to ensembles with AASIST3 as a second audio detector — dramatically improves robustness and reduces adversarial vulnerability.

3. **Vietnamese Localization**: Added explicit priority for Vietnamese scam script fine-tuning, as Vietnamese-language scams targeting elderly parents are the most critical real-world threat in Vietnam/Southeast Asia.

4. **Pre-call Number Risk Check**: Added optional OSINT pre-screening of caller numbers against known scam databases (before the call even begins).

5. **RAG-Augmented LLM**: Original used LLM for raw transcript scoring. Added FAISS-backed RAG with known scam script library — reduces hallucination and improves detection of evolving scam patterns.

6. **Federated/Continual Learning**: Added architecture for learning from confirmed scam cases across users (privacy-preserving, opt-in) — this is the self-improvement engine that makes the system uniquely valuable over time.

7. **Cold-Start Problem Handling**: Added pre-call number lookup to partially address the 10-second blind spot at call start.

8. **Challenge Question Engine**: Original mentioned challenge questions but didn't specify the generation mechanism. Added Qwen-powered context-aware challenge generation that changes each session to prevent scripted responses.

---

*Document Version: 1.0 | Last Updated: 2025-06-01*
