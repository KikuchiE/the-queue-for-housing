from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm your bot 🤖\nSend /help to see what I can do.")

# /help command handler
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("I can echo your messages.\nJust type anything and I'll repeat it!")

# Echo handler for normal text messages
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f'You said: {update.message.text}')

# Main function
async def main():
    # Replace this with your actual Bot Token
    bot_token = "YOUR_TELEGRAM_BOT_TOKEN"

    # Create the application
    app = ApplicationBuilder().token(bot_token).build()

    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Start the bot
    print("Bot is running...")
    await app.run_polling()

# Entry point
if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
