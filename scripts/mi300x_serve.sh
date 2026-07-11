#!/usr/bin/env bash
# CLAUSE — serve Gemma on the AMD hackathon pod (ROCm 7.2 + vLLM 0.16.0 image).
# Post-H6 sidequest per KICKOFF: same app, Gemma on AMD Instinct via vLLM/ROCm,
# swapped in with a single env var (DEC-003).
#
# Paste into a terminal on the pod (JupyterLab: File > New > Terminal).
set -euo pipefail

MODEL="${MODEL:-google/gemma-4-31b-it}"   # any served Gemma variant works (DEC-004)
PORT="${PORT:-8000}"

echo ">>> GPU check"
rocm-smi || true

echo ">>> Serving $MODEL with vLLM on ROCm (first run downloads weights — allow ~10-20 min)"
# --max-model-len keeps KV cache modest; adjudication inputs are <32k tokens.
vllm serve "$MODEL" \
  --host 0.0.0.0 \
  --port "$PORT" \
  --max-model-len 32768

# Once "Uvicorn running" appears, from the CLAUSE side set:
#   OPENAI_BASE_URL=http://<pod-address>:$PORT/v1
#   MODEL_ID=$MODEL
# and verify with: python scripts/smoke_test.py
