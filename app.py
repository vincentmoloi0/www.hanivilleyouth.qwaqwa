import os
from flask import Flask, request
import requests

app = Flask(__name__)

# Set these in Replit Secrets (Tools > Secrets)
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "my_verify_token")
PAGE_ACCESS_TOKEN = os.environ.get("PAGE_ACCESS_TOKEN")

@app.route('/')
def home():
    return "Bot is running on Replit!", 200

@app.route('/webhook', methods=['GET'])
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    return "Failed", 403

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if data.get("object") == "page":
        for entry in data.get("entry", []):
            for event in entry.get("messaging", []):
                sender = event["sender"]["id"]
                if "message" in event and "text" in event["message"]:
                    text = event["message"]["text"]
                    reply = f"Got it on Replit: {text}"
                    send(sender, reply)
    return "ok", 200

def send(recipient, text):
    url = f"https://graph.facebook.com/v19.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
    requests.post(url, json={"recipient": {"id": recipient}, "message": {"text": text}})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)