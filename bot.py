from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes
)

from config import settings


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        "🤖 Telegram Bot Platform\n\n"
        "Mini App খুলতে নিচের Web App ব্যবহার করুন।"
    )


def create_bot():

    app = Application.builder().token(
        settings.TELEGRAM_BOT_TOKEN
    ).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    return app


if __name__ == "__main__":

    application = create_bot()

    application.run_polling()
