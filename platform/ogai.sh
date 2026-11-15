#!/usr/bin/env bash
# 작은 시안 = 맥스튜디오 로컬 Z-Image Turbo(Open Generative AI 엔진, 무료). 노트북에서 SSH로 생성하고 결과를 가져온다.
# 사용: platform/ogai.sh "프롬프트" [폭 높이] [저장경로.png]   (기본 1344×576 = 21:9, 16의 배수로)
# 맥 1344×576 한 장 ≈ 42초. 큰 작업(360° 이어 그리기 · 영상 · 최종본)은 Higgsfield.
set -euo pipefail
[ $# -ge 1 ] || { echo "사용: $0 \"프롬프트\" [폭 높이] [저장경로.png]" >&2; exit 2; }
P="$1"; W="${2:-1344}"; H="${3:-576}"; OUT="${4:-./ogai_$(date +%Y%m%d_%H%M%S).png}"
MAC="${OGAI_HOST:-apple@mac-studio}"; SEED="${OGAI_SEED:--1}"
B64=$(printf %s "$P" | base64 | tr -d '\n'); NAME="ogai_$(date +%s%N).png"

ssh -o BatchMode=yes -o ConnectTimeout=8 "$MAC" "L=\"\$HOME/Library/Application Support/open-generative-ai/local-ai\"; M=\"\$L/models\"; mkdir -p ~/ogai_out
\"\$L/bin/sd-cli\" --diffusion-model \"\$M/z_image_turbo-Q4_K.gguf\" --vae \"\$M/ae.safetensors\" --llm \"\$M/Qwen3-4B-Instruct-2507-UD-Q4_K_XL.gguf\" \
  -p \"\$(echo $B64 | base64 -d)\" --cfg-scale 1.0 --steps 8 --diffusion-fa -W $W -H $H --seed $SEED -o ~/ogai_out/$NAME > ~/ogai_out/last.log 2>&1 \
  || { tail -5 ~/ogai_out/last.log; exit 1; }"
scp -q -o BatchMode=yes "$MAC:ogai_out/$NAME" "$OUT"
echo "$OUT"
