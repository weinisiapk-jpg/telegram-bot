import os
import logging
from flask import Flask, request
import telegram
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters

# 配置
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8665590058:AAEe6WMdo82jeruoRcs4o7a3S4oPVTv42Vc")
PORT = int(os.environ.get('PORT', 5000))

# Flask 应用
app = Flask(__name__)

# Bot 和 Dispatcher
bot = telegram.Bot(token=TOKEN)
dispatcher = Dispatcher(bot, None, workers=0)

def get_ai_response(message):
    responses = {
        "你好": "你好！我是你的 AI 助手！",
        "help": "发送消息给我，我会回复你！",
    }
    for key, value in responses.items():
        if key in message.lower():
            return value
    return f"收到：{message}\n\n（模拟回复，可接入真实AI）"

def start(update, context):
    update.message.reply_text("👋 你好！我是AI助手，直接发消息给我即可！")

def help_cmd(update, context):
    update.message.reply_text("可用命令：/start /help")

def handle_msg(update, context):
    ai_response = get_ai_response(update.message.text)
    update.message.reply_text(ai_response)

# 注册处理器
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("help", help_cmd))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_msg))

@app.route('/')
def index():
    return "Bot is running!"

@app.route('/webhook', methods=['POST'])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return 'ok'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
