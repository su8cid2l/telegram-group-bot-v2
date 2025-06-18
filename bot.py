from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from telegram import Update, ChatPermissions
import random

# 🔐 Bot Token
TOKEN = "8008461886:AAEpxGDSebJ4rbyAcZQpvPwWmJjnN-yXAmc"

# 🎯 /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm alive and hosted on Render!")

# 🆘 /help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Commands: /ban /unban /mute\nReply to a user’s message to use them.")

# 🎭 Random Welcome Messages
WELCOME_MESSAGES = [
    "Welcome to the twisted world of ghouls and humans. Will you feast or be feasted upon?",
    "You’ve entered the 20th Ward. Don’t lose yourself... or your mask.",
    "Like Kaneki, you've now opened your eyes to a new world. Welcome.",
    "This isn’t Anteiku, but we serve a warm welcome. Just... don't ask what's brewing.",
    "Even ghouls need company. Welcome to the shadows."
]

# 🎉 Welcome new members
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for user in update.message.new_chat_members:
        message = random.choice(WELCOME_MESSAGES)
        await update.message.reply_text(message)

# 🚫 /ban command
async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
        await context.bot.ban_chat_member(chat_id=update.effective_chat.id, user_id=user_id)
        await update.message.reply_text("User has been banned. 🚫")
    else:
        await update.message.reply_text("Reply to a user's message to ban them.")

# 🔇 /mute command
async def mute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
        permissions = ChatPermissions(can_send_messages=False)
        await context.bot.restrict_chat_member(
            chat_id=update.effective_chat.id,
            user_id=user_id,
            permissions=permissions
        )
        await update.message.reply_text("User has been muted. 🔇")
    else:
        await update.message.reply_text("Reply to a user's message to mute them.")

# 🔓 /unban command
async def unban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
        await context.bot.unban_chat_member(chat_id=update.effective_chat.id, user_id=user_id)
        await update.message.reply_text("User has been unbanned. 🔓")
    else:
        await update.message.reply_text("Reply to a user's message to unban them.")

# 🚀 Main app
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("ban", ban))
    app.add_handler(CommandHandler("mute", mute))
    app.add_handler(CommandHandler("unban", unban))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))
    app.run_polling()
