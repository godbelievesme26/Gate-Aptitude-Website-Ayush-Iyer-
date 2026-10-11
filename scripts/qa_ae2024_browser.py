import subprocess
import time
import json
import urllib.request
import base64
import os
import websocket

# Launch headless Chrome
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
user_data_dir = r"C:\Users\godbe\.gemini\antigravity\scratch\chrome_qa_2024"
port = 9228

cmd = [
    chrome_path,
    "--headless=new",
    f"--remote-debugging-port={port}",
    f"--user-data-dir={user_data_dir}",
    "--disable-gpu",
    "--no-first-run",
    "--no-default-browser-check",
    "about:blank"
]

proc = subprocess.Popen(cmd)
time.sleep(2)

def cdp_send(ws, method, params=None, msg_id=1):
    req = {"id": msg_id, "method": method, "params": params or {}}
    ws.send(json.dumps(req))
    while True:
        res = json.loads(ws.recv())
        if res.get("id") == msg_id:
            return res.get("result", {})

def capture_screenshot(ws, filename, msg_id=100):
    res = cdp_send(ws, "Page.captureScreenshot", {"format": "png"}, msg_id=msg_id)
    data = base64.b64decode(res["data"])
    out_path = os.path.join(r"C:\Users\godbe\.gemini\antigravity\brain\c05ba5de-1c22-4609-a6ec-bfdf2114d4f1", filename)
    with open(out_path, "wb") as f:
        f.write(data)
    print(f"Captured artifact: {filename}")
    return out_path

try:
    tabs = json.loads(urllib.request.urlopen(f"http://localhost:{port}/json").read())
    ws_url = tabs[0]["webSocketDebuggerUrl"]
    ws = websocket.create_connection(ws_url)

    cdp_send(ws, "Page.enable")
    cdp_send(ws, "DOM.enable")
    cdp_send(ws, "Emulation.setDeviceMetricsOverride", {
        "width": 1440,
        "height": 900,
        "deviceScaleFactor": 1,
        "mobile": False
    })

    # 1. Aerospace Hub
    print("Navigating to Aerospace Hub...")
    cdp_send(ws, "Page.navigate", {"url": "http://localhost:4173/#/aerospace"}, msg_id=2)
    time.sleep(2)
    capture_screenshot(ws, "ae2024_qa_01_hub.png", msg_id=101)

    # 2. AE2024 Paper Overview
    print("Navigating to AE2024 Paper Overview...")
    cdp_send(ws, "Page.navigate", {"url": "http://localhost:4173/#/aerospace/2024"}, msg_id=3)
    time.sleep(2)
    capture_screenshot(ws, "ae2024_qa_02_overview.png", msg_id=102)

    # 3. AE2024 Question Detail Q14 (has vibration response figure)
    print("Navigating to AE2024 Q14 (figure)...")
    cdp_send(ws, "Page.navigate", {"url": "http://localhost:4173/#/question/gate-2024-ae-ae-14"}, msg_id=4)
    time.sleep(2)
    capture_screenshot(ws, "ae2024_qa_03_q14_figure.png", msg_id=103)

    # 4. AE2024 Question Detail Q20 (option figures)
    print("Navigating to AE2024 Q20 (option figures)...")
    cdp_send(ws, "Page.navigate", {"url": "http://localhost:4173/#/question/gate-2024-ae-ae-20"}, msg_id=5)
    time.sleep(2)
    capture_screenshot(ws, "ae2024_qa_04_q20_option_figs.png", msg_id=104)

    # 5. AE2024 CBT Practice screen
    print("Navigating to AE2024 CBT...")
    cdp_send(ws, "Page.navigate", {"url": "http://localhost:4173/#/cbt/gate-2024-ae"}, msg_id=6)
    time.sleep(2)
    capture_screenshot(ws, "ae2024_qa_05_cbt.png", msg_id=105)

    ws.close()
    print("QA completed successfully!")
finally:
    proc.terminate()
