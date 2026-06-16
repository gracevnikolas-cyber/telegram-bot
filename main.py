import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# 🔐 токен берётся из Render Variables
TOKEN = os.getenv("TOKEN")

# 📌 ID админ-группы
ADMIN_GROUP_ID = -1003995942898


# 👋 старт
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Отправь сюда жалобу (текст или фото)."
    )


# 📩 обработка сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message:
        return

    user = message.from_user

    username = f"@{user.username}" if user.username else "без username"

    text = (
        "📩 ЖАЛОБА\n\n"
        f"👤 От: {username} | ID: {user.id} | {user.first_name}\n\n"
        f"📝 {message.text or message.caption or ''}"
    )

    try:
        # 📸 если фото
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
        await message.reply_text("❌ Ошибка при отправке")


# 🚀 запуск
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(filters.ChatType.PRIVATE & ~filters.COMMAND, handle_message)
    )

    print("Bot running...")
    app.run_polling()


if __name__ == "__main__":
    main()
