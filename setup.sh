#!/data/data/com.termux/files/usr/bin/bash

set -eu

echo "================================"
echo "  JARVIS - Termux Setup"
echo "================================"

if [ -z "${PREFIX:-}" ] || [ ! -d "$PREFIX" ]; then
    echo "Please run this script inside Termux."
    exit 1
fi

echo "[1/4] Updating package lists..."
pkg update

echo "[2/4] Installing dependencies..."
pkg install -y python git curl termux-api

echo "[3/4] Checking local AI files..."

MODEL="$HOME/models/qwen2.5-1.5b-instruct-q4_k_m.gguf"
SERVER="$HOME/llama.cpp/build/bin/llama-server"

if [ -f "$MODEL" ]; then
    echo "Qwen model found."
else
    echo "Qwen model not found at:"
    echo "$MODEL"
    echo "Download the compatible GGUF model separately."
fi

if [ -x "$SERVER" ]; then
    echo "llama-server found."
else
    echo "llama-server not found at:"
    echo "$SERVER"
    echo "Build llama.cpp separately before starting JARVIS."
fi

echo "[4/4] Checking Python..."
python --version

echo
echo "Setup checks complete!"
echo "Start the AI server separately, then run:"
echo "python $HOME/termux-local-ai-jarvis/jarvis.py"
