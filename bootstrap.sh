#!/usr/bin/env bash
set -e

# --- Create & activate venv ---
python -m venv .venv
source .venv/bin/activate

# --- Upgrade tooling ---
python -m pip install --upgrade pip setuptools wheel

# --- Install all dependencies ---
python -m pip install -r requirements.txt

# --- Optional: ensure .env exists ---
cp -n .env.example .env || true

# --- Pre-build FAISS index (for Lab 6, ok to skip if no data) ---
python -m labs.lab6_faiss_index.build_index --data data --out faiss_index || true

echo "✅ Environment ready. Activate with: source .venv/bin/activate"

source .venv/bin/activate
