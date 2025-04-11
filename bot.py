from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Define the start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Available commands:\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/echo - Echo your message\n"
        "Or just send any message, and I'll respond!"
    )

# Main function to run the bot
if __name__ == '__main__':
    # Replace 'YOUR_BOT_TOKEN_HERE' with your actual bot token from @BotFather
    TOKEN = '8186349035:AAFf-v08VFET2lylJj31Fptja-g0v-WO45k'
    app = ApplicationBuilder().token('8186349035:AAFf-v08VFET2lylJj31Fptja-g0v-WO45k').build()

    # Add a command handler for /start
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('help', help_command))

    # Run the bot until you press Ctrl+C
    app.run_polling()
