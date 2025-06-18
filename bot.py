from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

# 🔐 Bot token directly inserted for testing (not recommended for public use)
TOKEN = "8008461886:AAEpxGDSebJ4rbyAcZQpvPwWmJjnN-yXAmc"

# /start command
async def start(update, context):
    await update.message.reply_text("Hello! I'm alive and hosted on Render!")

# /help command
async def help_command(update, context):
    await update.message.reply_text("Use /start to begin. I can welcome users and echo messages!")

# Welcome new group members
async def welcome(update, context):
    for user in update.message.new_chat_members:
        await update.message.reply_text(f"Welcome, {user.first_name}! 🎉")

# Echo back any normal message
async def echo(update, context):
    await update.message.reply_text(f"You said: {update.message.text}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    app.run_polling()
