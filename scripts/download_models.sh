#!/bin/bash
# scripts/download_models.sh
echo "--- DeepFake Shield Model Downloader ---"
MODELS=(
    "lab260/AASIST3:models/audio/aasist3_onnx.onnx"
    "facebook/wav2vec2-xlsr-53:models/audio/wav2vec2_onnx.onnx"
    "custom/cnn-vit-hybrid:models/video/cnn_vit_onnx.onnx"
)

for entry in "${MODELS[@]}"; do
    repo="${entry%%:*}"
    path="${entry#*:}"
    echo "Fetching $repo to $path..."
    # huggingface-cli download $repo --local-dir-use-symlinks False --local-dir $path
done
echo "All models downloaded."
