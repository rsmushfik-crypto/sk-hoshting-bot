import os, sys, re, json, time, threading, subprocess
from pathlib import Path
from flask import Flask, request, jsonify
from flask_cors import CORS

# --- PATH ---
BASE_DIR = Path("data/bots")
BASE_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR = Path("logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)
META_FILE = Path("data/bots_meta.json")

app = Flask(__name__)
CORS(app)

running_bots = {} # bot_id -> process

# --- AUTO LIBRARY MAP ---
PIP_MAP = {
    "yt_dlp": "yt-dlp==2024.5.27",
    "telegram": "python-telegram-bot==20.7",
    "aiogram": "aiogram==3.3.0",
    "pyrogram": "pyrogram==2.0.106",
    "telethon": "telethon==1.34.0",
    "flask": "Flask==3.0.3",
    "requests": "requests==2.31.0",
    "PIL": "Pillow==10.3.0",
    "cv2": "opencv-python",
    "openai": "openai",
    "pymongo": "pymongo",
    "motor": "motor"
}

def log(bot_id, msg):
    print(f"[{bot_id}] {msg}")
    try:
        with open(LOG_DIR / f"{bot_id}.log", "a", encoding="utf-8") as f:
            f.write(f"{time.strftime('%H:%M:%S')} - {msg}\n")
    except: pass

def get_meta():
    if META_FILE.exists():
        try: return json.loads(META_FILE.read_text())
        except: return {}
    return {}

def save_meta(data):
    META_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2))

def detect_libs(code):
    found = set()
    for m in re.finditer(r'(?:from|import)\s+([a-zA-Z0-9_]+)', code):
        name = m.group(1)
        if name in PIP_MAP: found.add(PIP_MAP[name])
        if name.lower() in PIP_MAP: found.add(PIP_MAP[name.lower()])
    if not found: found.add("python-telegram-bot==20.7")
    return list(found)

def install_reqs(bot_id):
    bot_path = BASE_DIR / bot_id
    req_file = bot_path / "requirements.txt"
    if not req_file.exists():
        # যদি requirements না আসে, কোড থেকে বানাও
        code_file = bot_path / "main.py"
        if code_file.exists():
            libs = detect_libs(code_file.read_text(encoding="utf-8", errors="ignore"))
            req_file.write_text("\n".join(libs))
            log(bot_id, f"Auto requirements created: {libs}")
        else:
            return False
    try:
        log(bot_id, f"Installing {req_file.read_text()}")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "--no-cache-dir", "-r", str(req_file)],
            check=True, timeout=400
        )
        log(bot_id, "Install OK")
        return True
    except Exception as e:
        log(bot_id, f"Install Failed: {e}")
        return False

def run_bot(bot_id):
    bot_path = BASE_DIR / bot_id
    main_py = bot_path / "main.py"
    if not main_py.exists():
        log(bot_id, "main.py not found")
        return
    install_reqs(bot_id)
    env = os.environ.copy()
    meta = get_meta().get(bot_id, {})
    if "token" in meta:
        env["BOT_TOKEN"] = meta["token"]

    log(bot_id, f"Starting {main_py}")
    try:
        proc = subprocess.Popen(
            [sys.executable, str(main_py)],
            cwd=str(bot_path),
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        running_bots[bot_id] = proc
        for line in proc.stdout:
            log(bot_id, line.strip())
    except Exception as e:
        log(bot_id, f"CRASH: {e}")
    finally:
        running_bots.pop(bot_id, None)
        # Auto restart after 5 sec if folder still exists
        time.sleep(5)
        if (BASE_DIR / bot_id).exists():
            threading.Thread(target=run_bot, args=(bot_id,), daemon=True).start()

def start_watcher():
    # সার্ভার চালু হলে আগের সব বট চালাবে
    meta = get_meta()
    for bot_id in meta.keys():
        if bot_id not in running_bots:
            threading.Thread(target=run_bot, args=(bot_id,), daemon=True).start()

# --- API FOR YOUR HTML ---
@app.route("/")
def home():
    return jsonify({"status": "SK HOSTING POWERFUL", "running": list(running_bots.keys())})

@app.route("/bot/create", methods=["POST"])
def create_bot():
    data = request.json
    bot_id = data.get("id")
    token = data.get("token")
    code = data.get("code", "")
    requirements = data.get("requirements", "")

    bot_path = BASE_DIR / bot_id
    bot_path.mkdir(parents=True, exist_ok=True)

    (bot_path / "main.py").write_text(code, encoding="utf-8")

    # HTML থেকে requirements আসলে সেটা বসাও, না আসলে অটো ডিটেক্ট
    if not requirements:
        requirements = "\n".join(detect_libs(code))
    (bot_path / "requirements.txt").write_text(requirements, encoding="utf-8")

    meta = get_meta()
    meta[bot_id] = {
        "id": bot_id, "name": data.get("name"), "lang": data.get("lang"),
        "mask": data.get("mask"), "token": token,
        "status": "on", "until": data.get("until")
    }
    save_meta(meta)
    log(bot_id, f"Created with req: {requirements}")
    threading.Thread(target=run_bot, args=(bot_id,), daemon=True).start()
    return jsonify({"ok": True, "bot": meta[bot_id]})

@app.route("/bot/code", methods=["POST"])
def save_code():
    data = request.json
    bot_id = data.get("id")
    code = data.get("code")
    requirements = data.get("requirements", "")
    bot_path = BASE_DIR / bot_id
    if not bot_path.exists(): return jsonify({"ok": False, "error": "bot not found"})

    (bot_path / "main.py").write_text(code, encoding="utf-8")
    if not requirements:
        requirements = "\n".join(detect_libs(code))
    (bot_path / "requirements.txt").write_text(requirements, encoding="utf-8")

    log(bot_id, f"Code updated, new req: {requirements}")
    if data.get("restart") and bot_id in running_bots:
        running_bots[bot_id].terminate()
    else:
        threading.Thread(target=run_bot, args=(bot_id,), daemon=True).start()
    return jsonify({"ok": True})

@app.route("/bot/list", methods=["POST"])
def list_bots():
    meta = get_meta()
    return jsonify({"ok": True, "bots": list(meta.values())})

@app.route("/bot/start", methods=["POST"])
def start_bot():
    bot_id = request.json.get("id")
    if bot_id not in running_bots:
        threading.Thread(target=run_bot, args=(bot_id,), daemon=True).start()
    return jsonify({"ok": True})

@app.route("/bot/stop", methods=["POST"])
def stop_bot():
    bot_id = request.json.get("id")
    if bot_id in running_bots:
        running_bots[bot_id].terminate()
    return jsonify({"ok": True})

@app.route("/bot/delete", methods=["POST"])
def delete_bot():
    bot_id = request.json.get("id")
    if bot_id in running_bots:
        running_bots[bot_id].terminate()
    import shutil
    shutil.rmtree(BASE_DIR / bot_id, ignore_errors=True)
    meta = get_meta()
    meta.pop(bot_id, None)
    save_meta(meta)
    return jsonify({"ok": True})

@app.route("/bot/logs", methods=["POST"])
def bot_logs():
    bot_id = request.json.get("id")
    log_file = LOG_DIR / f"{bot_id}.log"
    logs = []
    if log_file.exists():
        logs = log_file.read_text(encoding="utf-8", errors="ignore").splitlines()[-200:]
    return jsonify({"ok": True, "log": logs})

@app.route("/bot/extend", methods=["POST"])
def extend_bot():
    data = request.json
    bot_id = data.get("id")
    meta = get_meta()
    if bot_id in meta:
        meta[bot_id]["until"] = data.get("until")
        meta[bot_id]["status"] = "on"
        save_meta(meta)
        if bot_id not in running_bots:
            threading.Thread(target=run_bot, args=(bot_id,), daemon=True).start()
    return jsonify({"ok": True, "until": data.get("until")})

@app.route("/ad/start", methods=["POST"])
def ad_start():
    return jsonify({"ok": True, "nonce": str(time.time())})

if __name__ == "__main__":
    threading.Thread(target=start_watcher, daemon=True).start()
    app.run(host="0.0.0.0", port=10000)
