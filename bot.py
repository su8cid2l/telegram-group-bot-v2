from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from telegram import Update
import random

# 🔐 Bot token (hardcoded — for testing only)
TOKEN = "8008461886:AAEpxGDSebJ4rbyAcZQpvPwWmJjnN-yXAmc"

# 🎯 /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm alive and hosted on Render!")

# 🆘 /help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Use /start to begin. I can welcome users and echo messages!")

# 🧛 Welcome new group members with random message
WELCOME_MESSAGES = [
    "Welcome to the twisted world of ghouls and humans. Will you feast or be feasted upon?",
    "You’ve entered the 20th Ward. Don’t lose yourself... or your mask.",
    "Like Kaneki, you've now opened your eyes to a new world. Welcome.",
    "This isn’t Anteiku, but we serve a warm welcome. Just... don't ask what's brewing.",
    "Even ghouls need company. Welcome to the shadows."
]

async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for user in update.message.new_chat_members:
        message = random.choice(WELCOME_MESSAGES)
        await update.message.reply_text(message)

# 🪞 Echo back any normal message
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"You said: {update.message.text}")

# 🚀 Start the bot
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    app.run_polling()
