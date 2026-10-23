import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler

TOKEN = os.environ.get("BOT_TOKEN")


async def start(update: Update, context):
    keyboard = [
        [InlineKeyboardButton("💰 My Balance", callback_data="balance")],
        [InlineKeyboardButton("📺 Watch Ads", callback_data="ads")],
        [InlineKeyboardButton("💸 Withdraw", callback_data="withdraw")]
    ]

    await update.message.reply_text(
        "🎉 Welcome to MoneyPlus Watch Earn!\n\nChoose an option:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def button(update: Update, context):
    query = update.callback_query
    await query.answer()

    if query.data == "balance":
        message = "💰 Your balance: $0.00\nDemo balance only."
    elif query.data == "ads":
        message = "📺 No advertising provider connected yet."
    else:
        message = "💸 Withdrawals are not enabled yet."

    await query.message.reply_text(message)


async def main():
    if not TOKEN:
        raise RuntimeError("Please set BOT_TOKEN in hosting environment")

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))

    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    try:
        await asyncio.Event().wait()
    finally:
        await app.updater.stop()
        await app.stop()
        await app.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
