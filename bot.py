from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from telegram import Update, ChatPermissions
import random
from datetime import timedelta

# 🔐 Bot Token
TOKEN = "8008461886:AAEpxGDSebJ4rbyAcZQpvPwWmJjnN-yXAmc"

# 🎯 /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm alive and hosted on Render!")

# 🆘 /help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Commands:\n/start, /help, /info, /rules, /setlang\n/ban, /unban, /mute, /unmute, /warn, /tban, /purge"
    )

# ℹ️ /info command
async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
        await update.message.reply_text(
            f"User Info:\nName: {user.full_name}\nID: {user.id}\nUsername: @{user.username if user.username else 'N/A'}"
        )
    else:
        await update.message.reply_text("Reply to a user's message to get their info.")

# 📜 /rules command
async def rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("These are the group rules. Be respectful, no spam, no hate.")

# 🌍 /setlang command (placeholder)
async def setlang(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Language settings will be available soon.")

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

# 🔈 /unmute command
async def unmute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
        permissions = ChatPermissions(
            can_send_messages=True,
            can_send_media_messages=True,
            can_send_other_messages=True,
            can_add_web_page_previews=True
        )
        await context.bot.restrict_chat_member(
            chat_id=update.effective_chat.id,
            user_id=user_id,
            permissions=permissions
        )
        await update.message.reply_text("User has been unmuted. 🔊")
    else:
        await update.message.reply_text("Reply to a user's message to unmute them.")

# 🔓 /unban command
async def unban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
        await context.bot.unban_chat_member(chat_id=update.effective_chat.id, user_id=user_id)
        await update.message.reply_text("User has been unbanned. 🔓")
    else:
        await update.message.reply_text("Reply to a user's message to unban them.")

# ⚠️ /warn command
warnings = {}

async def warn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
        warnings[user_id] = warnings.get(user_id, 0) + 1
        await update.message.reply_text(f"User warned! ⚠️ Total warnings: {warnings[user_id]}")
    else:
        await update.message.reply_text("Reply to a user's message to warn them.")

# ⏳ /tban command (temp ban in minutes)
async def tban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message and context.args:
        user_id = update.message.reply_to_message.from_user.id
        try:
            minutes = int(context.args[0])
            until_date = update.message.date + timedelta(minutes=minutes)
            await context.bot.ban_chat_member(
                chat_id=update.effective_chat.id,
                user_id=user_id,
                until_date=until_date
            )
            await update.message.reply_text(f"User temporarily banned for {minutes} minutes ⏳")
        except ValueError:
            await update.message.reply_text("Usage: /tban <minutes> (as a number)")
    else:
        await update.message.reply_text("Reply to a user and add minutes: /tban 10")

# 🧹 /purge command (delete N recent messages)
async def purge(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        count = int(context.args[0]) if context.args else 10
        messages = []
        async for msg in update.effective_chat.get_history(limit=count+1):
            messages.append(msg.message_id)
        await context.bot.delete_messages(chat_id=update.effective_chat.id, message_ids=messages)
    except Exception as e:
        await update.message.reply_text(f"Error purging: {e}")

# 🚀 Main app
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("info", info))
    app.add_handler(CommandHandler("rules", rules))
    app.add_handler(CommandHandler("setlang", setlang))
    app.add_handler(CommandHandler("ban", ban))
    app.add_handler(CommandHandler("unban", unban))
    app.add_handler(CommandHandler("mute", mute))
    app.add_handler(CommandHandler("unmute", unmute))
    app.add_handler(CommandHandler("warn", warn))
    app.add_handler(CommandHandler("tban", tban))
    app.add_handler(CommandHandler("purge", purge))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))
    app.run_polling()
