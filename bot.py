import os
import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from flask import Flask, request, jsonify

# Initialize Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Get environment variables
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
ALLOWED_USER_ID = os.getenv('ALLOWED_USER_ID')

# Koyeb API base URL
KOYEB_API_URL = "https://app.koyeb.com/v1"

# Verify user ID
def is_authorized(update: Update) -> bool:
    return str(update.message.from_user.id) == ALLOWED_USER_ID

# Function to make Koyeb API requests
def koyeb_request(method, endpoint, api_key, data=None):
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.request(method, f"{KOYEB_API_URL}{endpoint}", headers=headers, json=data)
    response.raise_for_status()
    return response.json()

# Command: /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        await update.message.reply_text("Unauthorized access.")
        return
    await update.message.reply_text("Hello! I'm your Koyeb manager bot.")

# Command: /logs
async def logs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        await update.message.reply_text("Unauthorized access.")
        return
    account = context.args[0] if context.args else None
    if not account:
        await update.message.reply_text("Usage: /logs <account>")
        return
    
    try:
        # Get API key and service ID from environment variables
        api_key = os.getenv(f"KOYEB_{account.upper()}_KEY")
        service_id = os.getenv(f"KOYEB_{account.upper()}_SERVICE")
        
        # Fetch logs from Koyeb API
        logs = koyeb_request("GET", f"/services/{service_id}/logs", api_key)
        await update.message.reply_text(logs[:4000])  # Send first 4000 characters
        
    except Exception as e:
        await update.message.reply_text(f"Error fetching logs: {str(e)}")

# Command: /redeploy
async def redeploy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        await update.message.reply_text("Unauthorized access.")
        return
    account = context.args[0] if context.args else None
    if not account:
        await update.message.reply_text("Usage: /redeploy <account>")
        return
    
    try:
        # Get API key and service ID from environment variables
        api_key = os.getenv(f"KOYEB_{account.upper()}_KEY")
        service_id = os.getenv(f"KOYEB_{account.upper()}_SERVICE")
        
        # Trigger redeploy
        koyeb_request("POST", f"/services/{service_id}/redeploy", api_key)
        await update.message.reply_text(f"Redeploy triggered for {account}.")
        
    except Exception as e:
        await update.message.reply_text(f"Error triggering redeploy: {str(e)}")

# Webhook endpoint
@app.route('/webhook', methods=['POST'])
async def webhook():
    update = Update.de_json(request.get_json(), bot)
    await application.process_update(update)
    return jsonify(success=True)

# Main function
if __name__ == '__main__':
    # Initialize Telegram bot
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Register command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("logs", logs))
    application.add_handler(CommandHandler("redeploy", redeploy))

    # Start Flask app
    app.run(host='0.0.0.0', port=8000)
