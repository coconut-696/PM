from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = "8726662807:AAEhyxd8epMeVuI82xT1_bCRCXXHUWChkCE"
ADMIN_ID = 7421114211


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام 👋\n"
        "به ربات پیام ناشناس خوش آمدی.\n"
        "پیامت را بفرست."
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    try:
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=(
                "📩 پیام جدید دریافت شد:\n\n"
                f"{user_message}"
            )
        )

        await update.message.reply_text(
            "پیامت ارسال شد ✅"
        )

    except Exception as e:
        print("ERROR:", e)

        await update.message.reply_text(
            "خطا در ارسال پیام ❌"
        )


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(
        CommandHandler("start", start)
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
