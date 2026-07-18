from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
TOKEN = "8726662807:AAElPtZ8HpqK7uMm0P8TKY-BZ0O1OzObAaM"
ADMIN_ID = 7421114211
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"📩 پیام جدید:\n\n{user_message}"
    )
    await update.message.reply_text(
        "پیامت ارسال شد ✅"
    )
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )
    app.run_polling()
if __name__ == "__main__":
    main()
