#!/usr/bin/env python
"""Generate + open a single combined Allure report from every device's results
under parallel/_output/allure-results/<udid>. Run after run_parallel.py."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_parallel import build_report  # noqa: E402

if __name__ == "__main__":
    build_report()
