#!/usr/bin/env bash
# Download Qwen3.5-4B GGUF weights (16-bit BF16 and Unsloth dynamic 2-bit Q2_K_XL).
# Usage: ./download_models.sh [output_dir]   (default: ./models)
# Set HF_TOKEN in the environment if you hit rate limits.
set -euo pipefail

REPO="unsloth/Qwen3.5-4B-GGUF"
OUT_DIR="${1:-./models}"
FILES=(
  "Qwen3.5-4B-BF16.gguf"
  "Qwen3.5-4B-UD-Q2_K_XL.gguf"
)

if ! command -v hf >/dev/null 2>&1; then
  echo "Installing huggingface_hub CLI..."
  python3 -m pip install --quiet --upgrade "huggingface_hub[cli]"
fi

mkdir -p "$OUT_DIR"
hf download "$REPO" "${FILES[@]}" --local-dir "$OUT_DIR"

echo "Downloaded to $OUT_DIR:"
ls -lh "${FILES[@]/#/$OUT_DIR/}"
