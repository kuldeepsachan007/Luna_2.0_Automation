#!/usr/bin/env python
"""
Luna Global Launcher  (cross-platform: Windows + macOS/Linux)

Ek shot me: backend ON -> cloudflared tunnel -> tunnel URL nikaalta hai ->
dashboard browser me khud khol deta hai. Dono OS par same chalta hai.

Chalane ke liye:
  Windows :  start_global.bat  (double-click)  ya:  python start_global.py
  macOS   :  ./start_global.sh                 ya:  python3 start_global.py
"""
import os
import re
import sys
import time
import socket
import shutil
import platform
import threading
import subprocess
import urllib.request
import webbrowser

ROOT   = os.path.dirname(os.path.abspath(__file__))
VERCEL = "https://luna-2-0-dashboard.vercel.app"
IS_WIN = platform.system() == "Windows"


def port_up(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    try:
        s.connect(("127.0.0.1", port))
        return True
    except Exception:
        return False
    finally:
        s.close()


def die(msg):
    print("  " + msg)
    try:
        input("Enter dabao band karne ke liye...")
    except Exception:
        pass
    sys.exit(1)


print("============ Luna Global Launcher ============")
print("     OS: " + platform.system())

# 1) BACKEND
if port_up(5000):
    print("[1/3] Backend already ON (127.0.0.1:5000)")
else:
    print("[1/3] Backend start ho raha hai...")
    out_dir = os.path.join(ROOT, "dashboard", "_output")
    os.makedirs(out_dir, exist_ok=True)
    bk = open(os.path.join(out_dir, "backend.log"), "w")
    subprocess.Popen([sys.executable, os.path.join(ROOT, "dashboard", "app.py")],
                     stdout=bk, stderr=subprocess.STDOUT)
    ok = False
    for _ in range(40):
        time.sleep(1)
        if port_up(5000):
            ok = True
            break
    if not ok:
        die("Backend start nahi hua. dashboard/_output/backend.log dekho.")
    print("      Backend ready.")

# 2) TUNNEL (cloudflared) -- OS ke hisaab se binary
if IS_WIN:
    cf = os.path.join(ROOT, "cloudflared.exe")
    if not os.path.exists(cf):
        print("      cloudflared.exe download ho raha hai (ek baar)...")
        try:
            urllib.request.urlretrieve(
                "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe",
                cf)
        except Exception as e:
            die("cloudflared download fail: " + str(e))
else:
    cf = shutil.which("cloudflared")
    if not cf:
        local = os.path.join(ROOT, "cloudflared")
        if os.path.exists(local):
            cf = local
        else:
            die("cloudflared nahi mila. Mac par install karo:  brew install cloudflared")

print("[2/3] Tunnel start ho raha hai...")
proc = subprocess.Popen([cf, "tunnel", "--url", "http://localhost:5000"],
                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                        text=True, bufsize=1)

url = None
for line in proc.stdout:
    m = re.search(r"https://[a-z0-9-]+\.trycloudflare\.com", line)
    if m:
        url = m.group(0)
        break
# baaki output background me drain karo taaki pipe na bhare
threading.Thread(target=lambda: [None for _ in proc.stdout], daemon=True).start()

if not url:
    die("Tunnel URL nahi mila.")
print("      Tunnel ready: " + url)

# 3) BROWSER
full = VERCEL + "/?api=" + url
try:
    webbrowser.open(full)
except Exception:
    pass

print("")
print("==================================================")
print(" SAB READY! Dashboard browser me khul gaya.")
print("")
print(" Vercel (share ke liye):")
print("   " + full)
print(" Direct (simple):")
print("   " + url)
print("")
print(" Is window ko BAND MAT karo (tunnel yahin chal raha hai).")
print(" Rokne ke liye Ctrl+C dabao.")
print("==================================================")

try:
    proc.wait()
except KeyboardInterrupt:
    proc.terminate()
