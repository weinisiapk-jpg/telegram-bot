import os
import logging
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, filters, CallbackContext

# 配置日志
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# 从环境变量读取
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8665590058:AAEe6WMdo82jeruoRcs4o7a3S4oPVTv42Vc")
PORT = int(os.environ.get('PORT', 5000))

# 创建 Flask 应用
app = Flask(__name__)

# 创建 Bot 和 Dispatcher
bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot, None, workers=0)

def get_ai_response(message: str) -> str:
    """简单的 AI 回复函数"""
    responses = {
        "你好": "你好！我是你的 AI 助手，有什么可以帮你的？",
        "help": "我可以帮你:\n1. 聊天对话\n2. 回答问题\n3. 辅助写作\n\n直接发送消息给我即可！",
        "你是谁": "我是你的透明 AI 助手，由我的主人设置来帮他处理消息。",
    }
    
    for key, value in responses.items():
        if key in message.lower():
            return value
    
    return f"我收到了你的消息：'{message}'\n\n（这是模拟回复。要接入真实 AI，请配置 API 密钥）"

def start(update: Update, context: CallbackContext):
    welcome = """👋 你好！我是 AI 助手

我是透明 AI 助手，由我的主人设置来帮他处理消息。

使用方法：
• 直接发送消息，我会自动回复
• /help - 查看帮助

注意：我是 AI，不是真人。"""
    update.message.reply_text(welcome)

def help_command(update: Update, context: CallbackContext):
    help_text = """🤖 AI 助手使用指南

可用命令：
/start - 开始使用
/help - 查看帮助

直接发送消息，我会回复你。"""
    update.message.reply_text(help_text)

def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text
    ai_response = get_ai_response(user_message)
    update.message.reply_text(ai_response)

# 注册处理器
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("help", help_command))
dispatcher.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

@app.route('/')
def index():
    return "Bot is running!"

@app.route('/webhook', methods=['POST'])
def webhook():
    """处理 Telegram webhook"""
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return 'ok'

@app.route('/set_webhook', methods=['GET'])
def set_webhook():
    """设置 webhook"""
    webhook_url = f"https://{request.host}/webhook"
    bot.set_webhook(url=webhook_url)
    return f"Webhook set to {webhook_url}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
