#!/usr/bin/env bash
# AI-STRIPPER 1-Click Launcher for macOS & Linux

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "========================================================"
echo "  AI-STRIPPER: Initializing Privacy Engine..."
echo "========================================================"
echo ""

# Check python3
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed!"
    echo "Please install Python 3 (e.g., brew install python or apt install python3 python3-pip)"
    exit 1
fi

# Install dependencies if missing
echo "[*] Checking dependencies..."
python3 -m pip install -q -r requirements.txt

# Launch interactive app
echo "[*] Launching AI-STRIPPER..."
echo ""
python3 stripper.py
