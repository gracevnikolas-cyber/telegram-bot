import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("TOKEN")
ADMIN_GROUP_ID = -1003995942898


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Отправь жалобу (текст или фото).")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message:
        return

    user = message.from_user
    username = f"@{user.username}" if user.username else "без username"

    text = (
        "📩 ЖАЛОБА\n\n"
        f"👤 {username} | ID: {user.id} | {user.first_name}\n\n"
        f"📝 {message.text or message.caption or ''}"
    )

    try:
        if message.photo:
            await context.bot.send_photo(
                chat_id=ADMIN_GROUP_ID,
                photo=message.photo[-1].file_id,
                caption=text
            )
        else:
            await context.bot.send_message(
                chat_id=ADMIN_GROUP_ID,
                text=text
            )

        await message.reply_text("✅ Отправлено")

    except Exception as e:
        print("ERROR:", e)
        await message.reply_text("❌ Ошибка")


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.ChatType.PRIVATE & ~filters.COMMAND, handle_message))

    print("Bot running...")
    app.run_polling()


if __name__ == "__main__":
    main()
