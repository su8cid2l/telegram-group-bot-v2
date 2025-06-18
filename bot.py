from telegram import Update, ChatPermissions
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os
import random
import time

TOKEN = os.environ.get("BOT_TOKEN")

# Random welcome messages
welcome_messages = [
    "Welcome to the twisted world of ghouls and humans. Will you feast or be feasted upon?",
    "You’ve entered the 20th Ward. Don’t lose yourself... or your mask.",
    "Like Kaneki, you've now opened your eyes to a new world. Welcome.",
    "This isn’t Anteiku, but we serve a warm welcome. Just... don't ask what's brewing.",
    "Even ghouls need company. Welcome to the shadows."
]

flood_limit = {}  # group_id: limit
filtered_words = {}  # group_id: [words]
locked_media = {}  # group_id: set of locked content types
user_message_log = {}  # (chat_id, user_id): [timestamps]
user_warns = {}  # (chat_id, user_id): warn_count

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm alive and hosted on Render!")

async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.new_chat_members:
        welcome_text = random.choice(welcome_messages)
        await update.message.reply_text(welcome_text)

# Ship command
async def ship(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        user1 = update.message.from_user.first_name
        user2 = update.message.reply_to_message.from_user.first_name
    else:
        members = await context.bot.get_chat_administrators(update.effective_chat.id)
        if len(members) < 2:
            await update.message.reply_text("Not enough members to ship!")
            return
        user1, user2 = random.sample(members, 2)
        user1 = user1.user.first_name
        user2 = user2.user.first_name

    percent = random.randint(0, 100)
    message = f❤️ Today's Ship:\n{user1} 💞 {user2} = {percent}%\n\n"
    if percent > 80:
        message += "Destiny brought them together. Or maybe just this bot."
    elif percent > 50:
        message += "They kinda vibe. OTP potential?"
    elif percent > 30:
        message += "Hmm. Some sparks... but will it last?"
    else:
        message += "Maybe just... friends. Probably."
    await update.message.reply_text(message)

# Warn command
async def warn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text("Reply to the user you want to warn.")
        return

    user = update.message.reply_to_message.from_user
    chat_id = update.effective_chat.id
    key = (chat_id, user.id)
    user_warns[key] = user_warns.get(key, 0) + 1
    warns = user_warns[key]
    await update.message.reply_text(f"⚠️ {user.first_name} has been warned. ({warns}/3)")
    if warns >= 3:
        try:
            await context.bot.ban_chat_member(chat_id, user.id)
            await update.message.reply_text(f"🚫 {user.first_name} has been kicked after 3 warnings.")
            user_warns[key] = 0
        except:
            await update.message.reply_text("Couldn't kick the user. Make sure I'm admin.")

async def resetwarns(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text("Reply to the user you want to reset warnings for.")
        return

    user = update.message.reply_to_message.from_user
    key = (update.effective_chat.id, user.id)
    user_warns[key] = 0
    await update.message.reply_text(f"✅ Warnings for {user.first_name} have been reset.")

# Ban command
async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text("Reply to the user you want to ban.")
        return
    try:
        await context.bot.ban_chat_member(update.effective_chat.id, update.message.reply_to_message.from_user.id)
        await update.message.reply_text("🚫 User banned successfully.")
    except:
        await update.message.reply_text("Failed to ban the user.")

# Unban command
async def unban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /unban <user_id>")
        return
    try:
        user_id = int(context.args[0])
        await context.bot.unban_chat_member(update.effective_chat.id, user_id)
        await update.message.reply_text("✅ User unbanned successfully.")
    except:
        await update.message.reply_text("Failed to unban the user.")

# Mute command
async def mute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text("Reply to the user you want to mute.")
        return
    try:
        permissions = ChatPermissions(can_send_messages=False)
        await context.bot.restrict_chat_member(update.effective_chat.id, update.message.reply_to_message.from_user.id, permissions)
        await update.message.reply_text("🔇 User muted successfully.")
    except:
        await update.message.reply_text("Failed to mute the user.")

# Flood protection
async def setflood(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /setflood <number>")
        return
    try:
        limit = int(context.args[0])
        flood_limit[update.effective_chat.id] = limit
        await update.message.reply_text(f"Flood limit set to {limit} messages per 5 seconds.")
    except:
        await update.message.reply_text("Invalid number.")

# Lock media
async def lock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /lock <media_type>")
        return
    media = context.args[0].lower()
    locked_media.setdefault(update.effective_chat.id, set()).add(media)
    await update.message.reply_text(f"Locked: {media}")

async def unlock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /unlock <media_type>")
        return
    media = context.args[0].lower()
    locked_media.get(update.effective_chat.id, set()).discard(media)
    await update.message.reply_text(f"Unlocked: {media}")

# Delete locked media messages
async def monitor_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    now = time.time()

    # Auto warn and kick
    if chat_id in flood_limit:
        key = (chat_id, user_id)
        user_message_log.setdefault(key, []).append(now)
        user_message_log[key] = [t for t in user_message_log[key] if now - t < 5]
        if len(user_message_log[key]) > flood_limit[chat_id]:
            user_warns[key] = user_warns.get(key, 0) + 1
            warns = user_warns[key]
            await update.message.reply_text(f"⚠️ {update.effective_user.first_name} warned for flooding. ({warns}/3)")
            if warns >= 3:
                try:
                    await context.bot.ban_chat_member(chat_id, user_id)
                    await update.message.reply_text(f"🚫 {update.effective_user.first_name} has been kicked for repeated flooding.")
                    user_warns[key] = 0
                except:
                    await update.message.reply_text("Failed to kick the user. Maybe I'm not admin?")

    locks = locked_media.get(chat_id, set())
    if "photo" in locks and update.message.photo:
        await update.message.delete()
    elif "video" in locks and update.message.video:
        await update.message.delete()
    elif "sticker" in locks and update.message.sticker:
        await update.message.delete()
    elif "document" in locks and update.message.document:
        await update.message.delete()

# Info command
async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    message = f"👤 User Info:\n"
    message += f"Name: {user.full_name}\n"
    message += f"Username: @{user.username}\n" if user.username else "Username: None\n"
    message += f"User ID: {user.id}\n"
    message += f"Chat ID: {chat.id}"
    await update.message.reply_text(message)

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))
    app.add_handler(CommandHandler("ship", ship))
    app.add_handler(CommandHandler("warn", warn))
    app.add_handler(CommandHandler("resetwarns", resetwarns))
    app.add_handler(CommandHandler("ban", ban))
    app.add_handler(CommandHandler("unban", unban))
    app.add_handler(CommandHandler("mute", mute))
    app.add_handler(CommandHandler("setflood", setflood))
    app.add_handler(CommandHandler("lock", lock))
    app.add_handler(CommandHandler("unlock", unlock))
    app.add_handler(CommandHandler("info", info))
    app.add_handler(MessageHandler(filters.ALL, monitor_media))

    app.run_polling()
