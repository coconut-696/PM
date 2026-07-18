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

users = {}
reply_targets = {}


def load_users():
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}


def save_users():
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=4)


users = load_users()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام 👋\nپیامت را بفرست."
    )


async def user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # اگر خود ادمین است، رد شو
    if update.effective_user.id == ADMIN_ID:
        return

    user_id = str(update.effective_user.id)
    text = update.message.text

    users[user_id] = True
    save_users()

    button = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton(
                "💬 پاسخ به کاربر",
                callback_data=f"reply:{user_id}"
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


async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.from_user.id != ADMIN_ID:
        return

    user_id = query.data.split(":")[1]

    reply_targets[ADMIN_ID] = user_id

    await query.message.reply_text(
        "✍️ پاسخ را بنویس:"
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
        CallbackQueryHandler(button_click)
    )

    # پیام‌های ادمین اول
    app.add_handler(
        MessageHandler(
            filters.User(ADMIN_ID) & filters.TEXT,
            admin_reply
        )
    )

    # پیام کاربران بعد
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            user_message
        )
    )

    app.run_polling()


if __name__ == "__main__":
    main()
