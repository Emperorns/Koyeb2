import os
import logging
import requests  # Add this import
from flask import Flask, request, jsonify
from telegram import Update
from app.auth import authenticate_request
from app.koyeb_cli import KoyebCLI

app = Flask(__name__)
koyeb = KoyebCLI()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        if not authenticate_request(request):
            logging.warning("Unauthorized webhook attempt")
            return jsonify({"status": "unauthorized"}), 403

        update = Update.de_json(request.get_json(), None)
        command = update.message.text.split()
        
        if command[0] == '/logs' and len(command) > 1:
            logs = koyeb.get_logs(command[1])
            send_telegram(update.message.chat.id, logs[:4000])  # Send first 4000 chars
            
        elif command[0] == '/redeploy' and len(command) > 1:
            status = koyeb.redeploy(command[1])
            send_telegram(update.message.chat.id, status)
            
        elif command[0] == '/list_services':
            services = koyeb.list_services()
            send_telegram(update.message.chat.id, services)
            
        else:
            send_telegram(update.message.chat.id, "Unknown command")

    except Exception as e:
        logging.error(f"Webhook error: {str(e)}")
        return jsonify({"status": "error"}), 500

    return jsonify({"status": "processed"}), 200

def send_telegram(chat_id, text):
    """Send a message via Telegram."""
    try:
        requests.post(
            f"https://api.telegram.org/bot{os.getenv('TELEGRAM_BOT_TOKEN')}/sendMessage",
            json={'chat_id': chat_id, 'text': str(text)}
        )
    except Exception as e:
        logging.error(f"Failed to send Telegram message: {str(e)}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
