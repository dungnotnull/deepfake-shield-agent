# SECOND-KNOWLEDGE-BRAIN.md
## DeepFake Shield Agent — Living Research Knowledge Base

> **What this file is:** A continuously self-updating knowledge base fed by automated crawling of arXiv, Semantic Scholar, ACL Anthology, and IEEE Xplore. It contains synthesized research findings, model benchmarks, and actionable insights that directly inform the agent's detection algorithms.
>
> **How it grows:** The `src/knowledge_updater/brain_updater.py` script appends new entries weekly. Entries are structured, citable, and cross-linked to source papers.
>
> **How agents use it:** Before implementing any detection component, consult the relevant section here. Search the FAISS index for semantic queries. Let this file prevent you from re-inventing the wheel or using outdated approaches.

---

## Table of Contents

1. [Audio Deepfake Detection](#1-audio-deepfake-detection)
2. [Video Deepfake Detection](#2-video-deepfake-detection)
3. [Multimodal Detection](#3-multimodal-detection)
4. [Scam & Phone Fraud Detection](#4-scam--phone-fraud-detection)
5. [On-Device Optimization](#5-on-device-optimization)
6. [Datasets & Benchmarks](#6-datasets--benchmarks)
7. [Active Anti-Spoofing Methods](#7-active-anti-spoofing-methods)
8. [Generalization & Robustness](#8-generalization--robustness)
9. [LLM for Fraud Detection](#9-llm-for-fraud-detection)
10. [Architecture Insights](#10-architecture-insights)
11. [Knowledge Update Log](#11-knowledge-update-log)

---

## 1. Audio Deepfake Detection

### 1.1 Key Models & Architectures

#### AASIST / AASIST3 (2021–2024)
- **What**: Anti-Spoofing with Adaptive Softmax and Instance-wise Temperature. Graph Attention Network-based architecture.
- **AASIST3 Enhancement**: KAN (Kolmogorov-Arnold Networks) + Wav2Vec2 SSL features + Graph Attention Networks. ASVspoof 2024 challenge system.
- **HuggingFace**: `lab260/AASIST3`
- **Key insight**: SSL features from Wav2Vec2 encoder provide significantly stronger representations than handcrafted features (MFCC) for zero-shot generalization.
- **Actionable for Shield**: Use AASIST3 as the primary audio detector. Its multi-branch inference is ideal for real-time ensemble scoring.
- **Source**: ASVspoof 2024 challenge; `lab260/AASIST3` model card.

#### Wav2Vec2-XLSR Deepfake Classifier
- **What**: Wav2Vec2 pretrained on 53 languages, fine-tuned for binary fake/real classification.
- **HuggingFace**: `Gustking/wav2vec2-large-xlsr-deepfake-audio-classification`
- **Fine-tuning approach**: Freeze feature extractor + bottom 12 transformer layers; train top 12 layers + classification head. Converges in ~3-4 epochs.
- **Architecture**: ~300M parameters; ~120ms inference on modern CPU.
- **Key insight**: Transfer learning from a specialist deepfake detector allows rapid adaptation with small local datasets.
- **Multilingual advantage**: XLSR-53 covers Vietnamese and other SE Asian languages — critical for Shield's target market.
- **Source**: `garystafford/wav2vec2-deepfake-voice-detector` model card (2024).

#### WavLM for Anti-Spoofing
- **What**: Alternative to Wav2Vec2; often outperforms on speaker-related tasks.
- **Key insight**: WavLM-Large shows superior cross-dataset generalization compared to Wav2Vec2-Large in some studies.
- **Recommendation**: Include WavLM as a third ensemble member if compute budget allows.
- **Source**: PyData Global 2024 presentation "Off-the-shelf HuggingFace models for audio deepfake detection".

#### RawNet2
- **What**: End-to-end model operating on raw waveforms. No handcrafted features needed.
- **Advantage**: Very lightweight; suitable for mobile deployment.
- **Limitation**: Lower accuracy than SSL-based models on out-of-distribution TTS.
- **Recommendation**: Use as mobile fallback when Wav2Vec2 cannot run.
- **Source**: ASVspoof 2019 challenge winner.

### 1.2 Feature Engineering Insights

- **MFCC (40–80 dim)**: Strong baseline, especially for codec-compressed audio (VoIP quality).
- **Mel-spectrogram (128 bins)**: Better captures spectral artifacts from neural vocoders.
- **High-frequency artifacts (>8kHz)**: TTS systems often have unnatural patterns above 8kHz. Include a high-frequency energy feature.
- **Phase spectrum anomalies**: TTS often has unnatural phase continuity. Phase-aware features improve detection.
- **GAN vs. Diffusion artifacts**: Diffusion-based TTS (2023+) is harder to detect via spectral methods alone — favor SSL-based approaches.
- **Key takeaway from Deepfake-Eval-2024**: Models trained on spectral/handcrafted features lose 48% AUC on in-the-wild 2024 samples. SSL-based models generalize significantly better.

### 1.3 Audio Detection Red Flags (Rule Layer)

The following patterns can be detected with fast rule-based methods (no ML needed) as a quick pre-filter:
- **Clipping artifacts**: Audio clipped at -0dBFS indicates resampling from TTS output
- **Silence patterns**: Unnatural silence before/after phonemes (TTS segmentation artifacts)
- **Background noise inconsistency**: Real calls have consistent background noise; TTS clones often lack it
- **Codec mismatch**: Vocoder artifacts + VoIP codec artifacts stack in distinguishable ways
- **Pitch variance flatness**: Human speech has natural pitch variation; TTS often has unnaturally flat pitch

---

## 2. Video Deepfake Detection

### 2.1 Key Architectures

#### CNN-ViT Hybrid (Springer 2026)
- **Reference**: "Hybrid deep learning architecture for real-time deepfake detection in WebRTC-based video platforms"
- **Architecture**: EfficientNet or ResNet (local spatial features) + Vision Transformer (global relationships)
- **Accuracy**: 98.33% on MIT DFD dataset; 98.97% precision; 99.70% on FaceForensics++
- **End-to-end latency**: 111–127ms within WebRTC pipeline — **meets our <150ms target**
- **Key insight**: CNN captures low-level artifacts (blending boundaries, texture inconsistencies) while ViT captures global face geometry — complementary strengths.
- **Actionable for Shield**: Use as primary video classifier. Fine-tune on FaceForensics++ + AV-Deepfake1M.
- **Source**: Springer Signal, Image and Video Processing, 2026.

#### GenConViT (2023)
- **What**: Generative Convolutional Vision Transformer. SOTA on academic datasets.
- **Limitation**: AUC drops ~50% on Deepfake-Eval-2024 in-the-wild data.
- **Recommendation**: Use CNN-ViT hybrid instead; GenConViT was trained on older manipulation techniques.

#### MediaPipe FaceMesh (Google)
- **What**: 468 3D facial landmarks at <2ms per frame on mobile.
- **Use cases**: Face detection (pre-filter), lip-sync alignment, gaze tracking, micro-expression analysis.
- **Key insight**: Landmark-based features (motion patterns, geometric consistency) generalize better across deepfake types than pixel-level features.
- **Actionable for Shield**: Use as lightweight pre-processor before running deep classifier.

### 2.2 Lip-Sync Detection

- **Audio-visual synchrony (AV offset)**: Real speech has ~0ms A-V offset; deepfake video often shows 50–200ms desynchrony.
- **Lip motion energy**: Unnatural ratio between phoneme energy and lip movement amplitude.
- **Viseme consistency**: Specific phonemes require specific mouth shapes (visemes). TTS + face-swap often misaligns these.
- **Implementation**: Compute mel-spectrogram energy per frame; compare against MediaPipe lip aperture distance. Pearson correlation < 0.6 is suspicious.
- **Source**: Mehrabi et al. (2024) multimodal detection study; ACM multimedia 2025.

### 2.3 Video Detection Red Flags (Rule Layer)

- **Eye blink frequency**: Deepfakes often blink less than humans (avg 15-20 blinks/min). Count via MediaPipe upper eyelid distance.
- **Facial boundary artifacts**: Blending artifacts around hairline, ears, and neck. Detectable via edge inconsistency.
- **Reflection inconsistency**: Skin reflection doesn't follow natural Lambertian model in synthesized faces.
- **Micro-tremor absence**: Natural faces have subtle muscle tremors; synthesized faces are unnaturally still.

---

## 3. Multimodal Detection

### 3.1 AV-Deepfake1M++ Dataset (2025)
- **Description**: Large-scale audio-visual deepfake dataset for classification and temporal localization.
- **Scale**: 1M+ samples covering lipsync, faceswap, voice clone, and diffusion-based manipulation.
- **Best system**: KLASSify (2025) — SSL audio backbone + graph attention networks for audio; handcrafted visual features. AUC 92.78% on classification, IoU 0.35 on temporal localization.
- **Key insight**: Multimodal systems consistently outperform single-modality by 5–15 AUC points under real-world distortions.
- **Source**: AV-Deepfake1M 2025 challenge; arxiv 2508.07337.

### 3.2 Cross-Modal Consistency Attacks
- **Problem**: Sophisticated attackers may manipulate only audio OR only video, knowing detectors focus on the other.
- **Mitigation**: Treat inconsistency between audio and video as its own detection signal. If audio is clean but video is synthetic, or vice versa: flag as suspicious.
- **Implementation**: Soft fusion — any single modality >0.75 contributes to alert even if others are low.

### 3.3 Temporal Context is Critical
- **Finding**: Per-frame or per-chunk detection misses gradual attacks where each individual frame/chunk is borderline.
- **Mitigation**: Maintain rolling 30-second risk window. A sustained score of 0.55 over 20+ seconds should trigger CAUTION even if no single chunk exceeds 0.70.
- **Implementation**: Exponential moving average of per-chunk scores with decay=0.85.

---

## 4. Scam & Phone Fraud Detection

### 4.1 State of the Problem (2024–2025)

- **Scale**: Phone scams siphoned $1.03 trillion globally in 2024 (2024 Global State of Scams Report).
- **Primary victims**: Elderly individuals; high susceptibility to urgency/authority tactics.
- **Deepfake integration**: Voice clone attacks now regularly use 3–10 second samples scraped from social media.
- **Trend**: LLM-generated scam scripts are emerging — adaptive, personalized, harder to detect with keyword lists alone.

### 4.2 LLM-Based Detection Approaches

#### "It Warned Me Just at the Right Moment" (2025)
- **Reference**: arxiv 2502.03964
- **Approach**: Real-time LLM analysis of phone call transcript; generates warnings during call.
- **Key finding**: LLMs detect subtle linguistic cues and conversational anomalies that rule-based systems miss.
- **Gap identified**: Relies solely on transcribed text; discards audio emotion/tone features.
- **Actionable for Shield**: Combine LLM transcript scoring WITH audio deepfake detection for superior coverage. This is exactly what Shield does.

#### SAFE-QAQ Framework
- **Reference**: ResearchGate 2025
- **Innovation**: Eliminates transcription error impact on detection performance. Rule-based slow-thinking reward mechanisms. Dynamic risk assessment during live calls.
- **Key metric**: Dramatic improvements on TeleAntiFraud-Bench over existing methods.
- **Actionable for Shield**: Adopt the sliding window risk accumulation approach from SAFE-QAQ. Implement in `risk_scorer.py`.

#### LLM-Augmented Expert Rules (EMNLP 2025)
- **Reference**: ACL Anthology 2025.findings-emnlp.270
- **Key insight**: Pure LLM approaches struggle with continuously evolving scam tactics (new scripts every few weeks). Hybrid LLM + expert rules significantly outperforms either alone.
- **Framework**: (1) Discrimination module → identifies scam characteristics; (2) Reflection module → reduces false positives by comparing with normal call features; (3) Summary step → synthesizes final score.
- **Actionable for Shield**: Implement this three-step approach in `risk_scorer.py`. The reflection step is critical for low false positive rates.

### 4.3 Common Vietnamese Scam Patterns

*(To be expanded as local data is collected)*

| Pattern | Keywords | Psychological Lever | Urgency Level |
|---|---|---|---|
| Family emergency | "con bị tai nạn", "em đang ở đồn", "bố bị bắt" | Fear/Parental instinct | CRITICAL |
| Bank security call | "tài khoản bị khóa", "giao dịch đáng ngờ" | Authority/Fear of loss | HIGH |
| Prize/lottery scam | "trúng thưởng", "cần đóng thuế trước" | Greed | HIGH |
| Government impersonation | "công an", "tòa án", "viện kiểm sát" | Authority/Fear | CRITICAL |
| Job offer scam | "việc làm online", "thu nhập cao" | Financial need | MEDIUM |
| Love scam | Extended relationship + financial request | Emotional attachment | MEDIUM |

### 4.4 Psychological Pressure Indicators (Rule Layer)

These patterns should trigger immediate HIGH risk score regardless of LLM output:
- Any request to transfer money in the current call (any amount)
- Requests for bank OTP/verification codes
- Instructions to "not tell" spouse/children/police
- Claims of legal emergency requiring immediate action
- Pressure to stay on the call and not hang up
- Requests to buy gift cards or cryptocurrency

---

## 5. On-Device Optimization

### 5.1 Model Compression Techniques

| Technique | Size Reduction | Accuracy Loss | Recommended For |
|---|---|---|---|
| INT8 Quantization | 4x | <1% EER increase | Audio models (Wav2Vec2) |
| FP16 | 2x | Minimal | All transformer models |
| Pruning (structured) | 2-4x | 1-3% | Less critical models |
| Knowledge Distillation | 5-10x | 5-10% | Mobile-primary deployment |
| ONNX Runtime | N/A (speed) | None | All models for cross-platform |
| TFLite | N/A (speed) | Minimal | Android/iOS deployment |

### 5.2 Inference Acceleration

- **CTranslate2 (Whisper)**: 2-4x faster than native HuggingFace for transformers. Use for Whisper ASR.
- **ONNX Runtime**: Best cross-platform option. Enables hardware acceleration on any device.
- **Core ML (iOS)**: Apple Neural Engine gives 5-10x speedup on A12+ chips for supported architectures.
- **NNAPI (Android)**: Delegates computation to hardware accelerator on Android 8.1+.
- **Batching**: Process audio chunks in micro-batches (4 chunks at once) to improve GPU utilization.

### 5.3 Memory Management

- **Audio buffer**: Circular buffer, 30 seconds max. Clear after session.
- **Video frames**: Process and discard. Never store more than 5 frames in RAM.
- **Model loading**: Load models once at startup, keep in RAM. Do NOT reload per-call.
- **FAISS index**: Memory-map large indexes to avoid RAM overhead.

---

## 6. Datasets & Benchmarks

### 6.1 Audio Datasets

| Dataset | Size | Languages | Deepfake Types | Use |
|---|---|---|---|---|
| ASVspoof 2019 LA | 2580 real + 22800 fake | English | TTS, VC | Training baseline |
| ASVspoof 2024 | Large-scale | English | TTS, VC, Diffusion | Primary eval |
| AV-Deepfake1M++ | 1M+ samples | Multilingual | Lipsync, voice clone | Large-scale eval |
| ADD 2023 | Medium | Chinese | TTS, VC + localization | Asian language support |
| FakeAVCeleb | 570 videos | English | TTS + face-swap | Multimodal baseline |

### 6.2 Video Datasets

| Dataset | Size | Deepfake Types | Year | Notes |
|---|---|---|---|---|
| FaceForensics++ | 1000 videos × 5 methods | Face2Face, DeepFakes, FaceSwap | 2019 | Classic benchmark; somewhat outdated |
| DeepFake Detection Challenge (DFDC) | 100k+ videos | Multiple | 2020 | Large scale, diverse |
| AV-Deepfake1M++ | 1M+ | Lipsync, faceswap, diffusion | 2024–2025 | Most current |
| Deepfake-Eval-2024 | 44h video + 56.5h audio | In-the-wild 2024 techniques | 2024 | **Best for generalization eval** |

### 6.3 Critical Benchmark: Deepfake-Eval-2024

**Finding**: Open-source SOTA models (GenConViT, AASIST, NPR) show 50% AUC decrease when evaluated on this in-the-wild benchmark vs academic datasets.

**Implication for Shield**: This is the strongest argument for the continuous self-learning architecture. Models trained only at release will degrade rapidly. Weekly model evaluation against newest samples is essential.

**Action items**:
1. Subscribe to Deepfake-Eval updates
2. Run monthly benchmark regression test
3. Trigger fine-tuning if AUC drops >5% vs. last measurement

---

## 7. Active Anti-Spoofing Methods

### 7.1 Corneal Reflection Probing

- **Reference**: Guo et al., University at Buffalo (2022). arxiv 2210.14153
- **Method**: Display a known pattern on screen; analyze corneal reflections in the eye for consistency with the displayed pattern. Real faces show accurate reflections; deepfakes cannot simulate this physics.
- **Advantage**: Generalization-independent — works regardless of which deepfake algorithm is used.
- **Limitation**: Requires the target to be visible (camera on) and have detectable corneal region.
- **Implementation**: Use MediaPipe to locate eye region; extract 64×64 crop; compare pattern correlation vs. expected reflection pattern.
- **False negative risk**: Poor lighting or small face size may make corneal region undetectable.

### 7.2 Gaze Consistency Probing

- **Reference**: arxiv 2509.25503 (2025)
- **Method**: During conversations, humans use gaze as nonverbal communication in predictable patterns. Real-time deepfakes cannot replicate this subtle behavior.
- **Key finding**: Gaze patterns during conversations follow specific statistical distributions that deepfakes violate.
- **Implementation**: Use MediaPipe iris tracking to estimate gaze direction per frame; compare gaze velocity and fixation distribution against human baseline.

### 7.3 SFake: Shake-Based Active Probing

- **Reference**: arxiv 2409.10889 (2024)
- **Method**: Inject a brief probe stimulus (visual or motion) and verify that the face responds consistently. Deepfake rendering pipeline introduces detectable latency.
- **Mobile-specific**: Designed for mobile devices, making it directly applicable to Shield's use case.
- **Advantage**: Works even against highly sophisticated face-swap systems.

### 7.4 Audio-Based Active Probing

*(Emerging — monitor for 2025 papers)*

- Concept: Play a specific sound stimulus and verify that the received audio shows appropriate spectral response (room acoustics). Synthesized audio cannot perfectly simulate acoustic environment response.
- Status: Experimental; not yet production-ready.

---

## 8. Generalization & Robustness

### 8.1 The Generalization Crisis

The Deepfake-Eval-2024 findings (2024) reveal a critical problem: SOTA models trained on academic datasets suffer severe performance degradation on real-world 2024 deepfakes:
- **Video AUC**: Drops by ~50%
- **Audio AUC**: Drops by ~48%
- **Image AUC**: Drops by ~45%

### 8.2 Why Models Fail to Generalize

1. **Training-Evaluation Mismatch**: Academic datasets contain outdated manipulation techniques (FaceForensics++ uses 2018-era methods).
2. **Compression Artifacts**: Real calls use codec compression (H.264, Opus) that alters deepfake artifacts in unpredictable ways.
3. **Diverse Content**: In-the-wild deepfakes span 52 languages, 88 websites — far more diverse than academic datasets.
4. **Arms Race**: Deepfake generators are specifically trained to defeat detectors.

### 8.3 Mitigation Strategies

| Strategy | Implementation | Effectiveness |
|---|---|---|
| Continuous re-evaluation | Monthly AUC benchmark | Detects degradation early |
| SSL-based features (Wav2Vec2, WavLM) | Use pre-trained representations | Better cross-domain generalization |
| Ensemble diversity | Use models with different architectures | Reduces simultaneous failure |
| Active probing | Corneal/gaze methods | Architecture-independent |
| Data augmentation (codec simulation) | Apply VoIP codec degradation to training data | Improves real-call robustness |
| Federated learning | Learn from real-world detected cases | Closes training-distribution gap |

### 8.4 Codec Robustness Testing

Shield operates on compressed VoIP/WebRTC streams. Models should be tested and fine-tuned with:
- **Audio codecs**: Opus, G.711, G.729, AMR-WB (WhatsApp, Zalo, VoIP)
- **Video codecs**: H.264, VP8, VP9 (WebRTC standard)
- **Bandwidth conditions**: 50kbps, 128kbps, 256kbps, 1Mbps (realistic network conditions)

---

## 9. LLM for Fraud Detection

### 9.1 Model Selection for Shield

| Model | Size | Context | Vietnamese | Local? | Recommendation |
|---|---|---|---|---|---|
| Qwen2.5-7B-Instruct | 7B (Q4: 4.7GB) | 128K tokens | Excellent | Ollama ✓ | **Primary choice** |
| Qwen2.5-3B-Instruct | 3B (Q4: 2.2GB) | 32K tokens | Good | Ollama ✓ | **Mobile fallback** |
| Llama-3.2-3B-Instruct | 3B (Q4: 2.0GB) | 128K tokens | Limited | Ollama ✓ | English-only alternative |
| Gemma-2-2B-Instruct | 2B (Q4: 1.5GB) | 8K tokens | Limited | Ollama ✓ | Lowest resource option |

**Why Qwen2.5**: Best Vietnamese + Chinese language support among local models; strong instruction following; fast inference; 128K context for long calls.

### 9.2 Prompt Engineering Insights

- **Chain-of-thought for fraud**: Prompting the LLM to reason step-by-step ("Is there urgency? Is there a money request? Is there identity claiming?") significantly improves precision over direct classification.
- **Negative examples**: Including 2-3 examples of legitimate-sounding calls in the system prompt reduces false positives.
- **Risk score granularity**: 0-100 scale with explicit thresholds outperforms categorical labels (scam/not-scam) for nuanced detection.
- **Temperature**: Use temperature=0 or 0.1 for fraud scoring (deterministic); higher temperature for challenge question generation (diversity).

### 9.3 RAG for Evolving Scam Scripts

- **Problem**: Scammers change scripts every few weeks to defeat trained models.
- **Solution**: FAISS-backed RAG that automatically adds new confirmed scam scripts to the retrieval corpus.
- **Retrieval approach**: Semantic similarity search (sentence-transformers) to find similar past scam patterns.
- **Augmentation**: Inject top-3 similar scam patterns into the LLM prompt as few-shot examples.
- **Key insight from EMNLP 2025**: RAG-augmented LLM detects new scam variants 3-4 weeks faster than fine-tuned models alone.

---

## 10. Architecture Insights

### 10.1 Latency vs. Accuracy Tradeoffs

Based on reviewed papers and benchmarks:

| Component | Speed-first option | Accuracy-first option |
|---|---|---|
| Audio detection | AASIST (80ms, EER~5%) | Wav2Vec2-XLSR (120ms, EER~3%) |
| Video detection | MobileNet+FaceMesh (30ms, AUC 0.85) | CNN-ViT (110ms, AUC 0.98) |
| Scam scoring | Rule-based (5ms, P~0.80) | Qwen2.5-7B (300ms, P~0.92) |
| ASR | Whisper-base (50ms) | Whisper-medium (200ms) |

**Shield strategy**: Use accuracy-first during non-critical periods; fall back to speed-first if latency budget exceeded.

### 10.2 False Positive Rate is the Critical UX Metric

Research consistently shows that detection systems fail in practice not due to low recall, but due to high false positive rates that cause user abandonment. Shield's design principle:

> **It is better to miss 15% of deepfakes than to incorrectly interrupt 1% of legitimate calls.**

Calibrate all thresholds with this priority. Use precision-first tuning on the validation set.

### 10.3 User Interface Design Principles

Based on UX research on security warning effectiveness:
- **Non-blocking default**: Show subtle indicator first; escalate only on high confidence.
- **Explain the risk**: Don't just say "Suspicious call" — say "Voice pattern inconsistencies detected."
- **Actionable**: Always give the user a clear action to take (hang up, ask challenge question, continue with caution).
- **Don't cry wolf**: Multiple false alarms train users to ignore all warnings. Precision over recall.

---

## 11. Knowledge Update Log

### Update 001 — 2025-06-01 (Manual Seed)

**Papers processed**: 15 key papers
**Models discovered**: AASIST3, Wav2Vec2-XLSR deepfake fine-tunes, CNN-ViT hybrid for WebRTC
**Key findings this cycle**:
- Deepfake-Eval-2024 reveals critical generalization gap — continuous update is existential for accuracy
- Active probing (corneal reflection, gaze) is the most robust anti-spoofing approach
- LLM hybrid + expert rules outperforms pure ML approaches for scam detection
- SAFE-QAQ framework advances the state of real-time fraud detection
- Vietnamese/multilingual support: Qwen2.5 is the clear best local model choice

**Model recommendations updated**: Added AASIST3 as primary audio model; added CNN-ViT hybrid as primary video model
**Prompt updates**: Scam detection system prompt refined based on SAFE-QAQ slow-thinking approach
**Action items generated**:
- [ ] Download and evaluate `lab260/AASIST3`
- [ ] Collect Vietnamese TTS samples for evaluation
- [ ] Implement corneal reflection probing from arxiv 2210.14153
- [ ] Test Qwen2.5-7B on Vietnamese scam transcripts

---

### Update Template (for `brain_updater.py`)

```markdown
### Update NNN — YYYY-MM-DD (Auto)

**Query terms used**: [list]
**Papers processed**: N
**New models discovered**: [list with HuggingFace IDs if available]
**Key findings this cycle**:
- Finding 1 + actionable recommendation
- Finding 2 + actionable recommendation

**Model recommendations updated**: [what changed]
**Prompt updates**: [what changed in system prompts]
**Action items generated**:
- [ ] Action item 1
- [ ] Action item 2
```

---

*Knowledge base maintained by `src/knowledge_updater/brain_updater.py`*
*FAISS index location: `./knowledge/faiss.index`*
*Embedding model: `sentence-transformers/all-mpnet-base-v2`*
*Next scheduled update: Weekly, Monday 02:00 UTC*
