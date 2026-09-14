#!/bin/bash
# Luna dashboard backend (macOS/Linux). Windows par run_dashboard.bat use karo.
# Ek baar executable banao:  chmod +x dashboard/run_dashboard.sh
# Phir chalao:  ./dashboard/run_dashboard.sh
cd "$(dirname "$0")/.."
if [ -f venv/bin/activate ]; then
  source venv/bin/activate
elif [ -f myenv/bin/activate ]; then
  source myenv/bin/activate
fi
echo "Dashboard -> http://127.0.0.1:5000  (Ctrl+C to stop)"
python3 dashboard/app.py
