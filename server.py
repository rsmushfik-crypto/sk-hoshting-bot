import os, subprocess, sys

# অটো ইনস্টল - যেটা মিসিং থাকবে সেটাই ইনস্টল হবে
def install(package):
    try: __import__(package.split('==')[0].replace('-', '_').replace('python_telegram_bot', 'telegram'))
    except:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install("python-telegram-bot==20.7")
install("yt-dlp==2024.5.27")

from flask import Flask, request, jsonify
from flask_cors import CORS
import threading, uuid

app = Flask(__name__)
CORS(app)

def run_bot(bot_id, code, token):
    bot_dir = f"/tmp/{bot_id}"
    os.makedirs(bot_dir, exist_ok=True)
    # বটের জন্য আলাদা requirements
    with open(f"{bot_dir}/requirements.txt", "w") as f:
        f.write("python-telegram-bot==20.7\nyt-dlp==2024.5.27\n")
    subprocess.call([sys.executable, "-m", "pip", "install", "-r", f"{bot_dir}/requirements.txt", "-q"])

    with open(f"{bot_dir}/main.py", "w", encoding="utf-8") as f:
        f.write(code)
    env = os.environ.copy()
    env["BOT_TOKEN"] = token
    subprocess.Popen([sys.executable, "main.py"], cwd=bot_dir, env=env)

@app.route('/')
def home(): return "SK HOSTING LIVE - v2 Fixed"

@app.route('/start_bot', methods=['POST'])
def start_bot():
    data = request.json
    bot_id = str(uuid.uuid4())[:10]
    t = threading.Thread(target=run_bot, args=(bot_id, data['code'], data['token']))
    t.start()
    return jsonify({"status": "started", "bot_id": bot_id})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
