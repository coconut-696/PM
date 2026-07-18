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

# ذخیره ارتباط کاربرها (موقت)
users = {}

# کاربرها و حالت پاسخ دادن ادمین
reply_mode = None


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام 👋\n"
        "پیامت را بفرست. پیام تو ناشناس ارسال می‌شود."
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global reply_mode

    user_id = update.effective_user.id
    text = update.message.text

    # اگر ادمین در حالت پاسخ باشد
    if update.effective_user.id == ADMIN_ID and reply_mode:
        target_user = reply_mode

        await context.bot.send_message(
            chat_id=target_user,
            text=f"📩 پاسخ:\n\n{text}"
        )

        reply_mode = None

        await update.message.reply_text(
            "پاسخ ارسال شد ✅"
        )
        return

    # پیام کاربر معمولی
    users[user_id] = True

    button = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "پاسخ به کاربر",
                    callback_data=f"reply_{user_id}"
                )
            ]
        ]
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
    global reply_mode

    query = update.callback_query
    await query.answer()

    if query.from_user.id != ADMIN_ID:
        return

    user_id = int(query.data.split("_")[1])

    reply_mode = user_id

    await query.message.reply_text(
        "✍️ پاسخ خود را بنویس:"
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

    app.run_polling()


if __name__ == "__main__":
    main()
