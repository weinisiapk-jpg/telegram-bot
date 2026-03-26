import os
import asyncio
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8665590058:AAEe6WMdo82jeruoRcs4o7a3S4oPVTv42Vc")

def get_ai_response(message: str) -> str:
    responses = {
        "你好": "你好！我是你的 AI 助手，有什么可以帮你的？",
        "help": "我可以帮你:\n1. 聊天对话\n2. 回答问题\n3. 辅助写作\n\n直接发送消息给我即可！",
        "你是谁": "我是你的透明 AI 助手，由我的主人设置来帮他处理消息。",
    }
    for key, value in responses.items():
        if key in message.lower():
            return value
    return f"我收到了你的消息：'{message}'\n\n（这是模拟回复。要接入真实 AI，请配置 API 密钥）"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome = """👋 你好！我是 AI 助手

我是透明 AI 助手，由我的主人设置来帮他处理消息。

使用方法：
• 直接发送消息，我会自动回复
• /help - 查看帮助

注意：我是 AI，不是真人。"""
    await update.message.reply_text(welcome)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """🤖 AI 助手使用指南

可用命令：
/start - 开始使用
/help - 查看帮助

直接发送消息，我会回复你。"""
    await update.message.reply_text(help_text)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    ai_response = get_ai_response(user_message)
    await update.message.reply_text(ai_response)

async def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
