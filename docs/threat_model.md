# Threat Model: DeepFake Shield Agent

## 1. Adversary Profile
- **Capability**: High. Access to SOTA TTS (ElevenLabs), Face-Swap (DeepFaceLive), and LLM-driven social engineering scripts.
- **Goal**: Financial fraud via emotional manipulation and impersonation.

## 2. Attack Surfaces
- **Voice Channel**: Synthesized speech targeting elderly users via VoIP.
- **Video Channel**: Real-time face-swapping over WebRTC (Zoom, WhatsApp).
- **Linguistic Channel**: Use of high-pressure, urgent scripts to bypass rational thinking.

## 3. Mitigation Strategy
- **Audio**: Detect spectral artifacts via AASIST3 and Wav2Vec2.
- **Video**: Detect geometric inconsistencies via CNN-ViT and physical impossibilities via corneal reflection.
- **Linguistic**: Semantic analysis of intent and request patterns via Qwen2.5.
- **Fusion**: Temporal risk accumulation to prevent "borderline" attacks from passing.
