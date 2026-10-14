# Termux Local AI — JARVIS

A local AI assistant experiment on Android using Termux, Python,
llama.cpp, and Qwen 2.5 1.5B.

## Features
- Local Qwen AI through llama.cpp
- Python JARVIS assistant
- YouTube search shortcuts
- Camera and Wi-Fi settings shortcuts
- Battery status with Termux:API
- Android text-to-speech responses

## Requirements
- Android and Termux
- Python 3 and Termux:API
- llama.cpp and a compatible Qwen GGUF model

## Start the AI server

Run in Termux:

    cd ~/llama.cpp
    ./build/bin/llama-server -m ~/models/qwen2.5-1.5b-instruct-q4_k_m.gguf --host 127.0.0.1 --port 8080 -c 2048 -t 4

## Start JARVIS

In another Termux session:

    python ~/termux-local-ai-jarvis/jarvis.py

The model file is intentionally not included in this repository.
