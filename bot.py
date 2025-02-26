import os
import logging
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

# Verify user ID
def is_authorized(update: Update) -> bool:
    return str(update.message.from_user.id) == ALLOWED_USER_ID

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
    # Add your Koyeb API logic here
    await update.message.reply_text(f"Fetching logs for {account}...")

# Command: /redeploy
async def redeploy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        await update.message.reply_text("Unauthorized access.")
        return
    account = context.args[0] if context.args else None
    if not account:
        await update.message.reply_text("Usage: /redeploy <account>")
        return
    # Add your Koyeb API logic here
    await update.message.reply_text(f"Redeploying {account}...")

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
