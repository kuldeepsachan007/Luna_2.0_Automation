#!/bin/bash
# Luna Global Launcher (macOS/Linux). Windows par start_global.bat use karo.
# Pehle ek baar executable banao:  chmod +x start_global.sh
# Phir chalao:  ./start_global.sh
cd "$(dirname "$0")"
if [ -f venv/bin/activate ]; then
  source venv/bin/activate
elif [ -f myenv/bin/activate ]; then
  source myenv/bin/activate
fi
python3 start_global.py
