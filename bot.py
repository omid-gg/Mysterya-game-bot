import os
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import requests
from flask import Flask, jsonify

load_dotenv()

TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# دستور استارت
def start(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id  # دریافت چت آیدی از پیام
    update.message.reply_text(
        f"سلام {update.effective_user.first_name}! خوش اومدی. آماده بازی هستی؟"
    )

def play(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("بازی شروع شد! موفق باشی.")

app = Flask(__name__)

@app.route('/start_game', methods=['POST'])
def start_game():
  
    updater = Updater(TELEGRAM_API_TOKEN)
    dispatcher = updater.dispatcher
    for user in dispatcher.chat_data.keys():
        chat_id = user 
        bot = requests.get(f'https://api.telegram.org/bot{TELEGRAM_API_TOKEN}/sendMessage', params={
            'chat_id': chat_id, 
            'text': 'بازی شروع شد! مبارزات آغاز می‌شود.'
        })
        if bot.status_code != 200:
            return jsonify({"status": "error", "message": "Failed to start game"}), 400
    return jsonify({"status": "success", "message": "Game started!"})

if __name__ == '__main__':
    # تنظیمات برای اجرا در حالت تولید
    app.run(debug=False, host='0.0.0.0', port=5000)
