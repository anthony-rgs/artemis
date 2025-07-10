#!/bin/bash

echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

echo "🌐 Installing Playwright and browsers..."
python -m playwright install --with-deps

echo "🚀 Starting your app..."
python3 billion_club.py