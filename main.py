import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

TOKEN = "8726662807:AAEhyxd8epMeVuI82xT1_bCRCXXHUWChkCE"
ADMIN_ID = 7421114211

DB_FILE = "database.json"


def load_db():
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}


def save_db(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


users = load_db()
reply_targets = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام 👋\n"
        "پیامت را بفرست. پیام تو ناشناس ارسال می‌شود."
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    text = update.message.text

    users[user_id] = True
    save_db(users)

    button = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton(
                "💬 پاسخ به کاربر",
                callback_data=f"reply_{user_id}"
            )
        ]]
    )

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"📩 پیام جدید:\n\n{text}",
        reply_markup=button
    )

    await update.message.reply_text(
        "پیامت ارسال شد ✅"
    )


async def reply_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.from_user.id != ADMIN_ID:
        return

    user_id = query.data.replace("reply_", "")

    reply_targets[ADMIN_ID] = user_id

    await query.message.reply_text(
        "✍️ پاسخ خود را بنویس:"
    )


async def admin_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    if ADMIN_ID not in reply_targets:
        return

    user_id = reply_targets[ADMIN_ID]

    await context.bot.send_message(
        chat_id=int(user_id),
        text=f"📩 پاسخ:\n\n{update.message.text}"
    )

    del reply_targets[ADMIN_ID]

    await update.message.reply_text(
        "پاسخ ارسال شد ✅"
    )


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(
        CallbackQueryHandler(reply_button)
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message
        )
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & filters.User(ADMIN_ID),
            admin_reply
        )
    )

    app.run_polling()


if __name__ == "__main__":
    main()
