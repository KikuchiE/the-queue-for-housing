from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv
import requests
import os

load_dotenv()

API_URL = "http://localhost:8000/api/check-queue/" 
# Define the start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Available commands:\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/echo - Echo your message\n"
        "/check_queue_position <IIN> - Check your queue position by IIN\n"
        "Or just send any message, and I'll respond!"
    )

async def check_queue_position(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Get the arguments (IIN) provided after the command
    if not context.args:
        await update.message.reply_text("Please provide an IIN. Usage: /check_queue_position <IIN>")
        return
    
    iin = context.args[0]  # Take the first argument as the IIN
    
    # Validate IIN (basic check for length, adjust as needed)
    if len(iin) != 12 or not iin.isdigit():
        await update.message.reply_text("Invalid IIN. It should be a 12-digit number.")
        return
    
    try:
        # Make POST request to your API
        response = requests.post(API_URL, json={"iin": iin})
        
        # Check the response status
        if response.status_code == 200:
            data = response.json()
            queue_position = data.get("queue_position")
            await update.message.reply_text(f"Your queue position is: {queue_position}")
        elif response.status_code == 404:
            data = response.json()
            await update.message.reply_text(data.get("message", "No user or application found."))
        else:
            await update.message.reply_text("Error checking queue position. Please try again later.")
            
    except requests.exceptions.RequestException:
        await update.message.reply_text("Failed to connect to the server. Please try again later.")

# Main function to run the bot
if __name__ == '__main__':
    # Replace 'YOUR_BOT_TOKEN_HERE' with your actual bot token from @BotFather
    TOKEN = os.getenv('TELEGRAM_TOKEN')
    print(TOKEN)
    app = ApplicationBuilder().token(TOKEN).build()

    # Add a command handler for /start
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('check_queue_position', check_queue_position))

    # Run the bot until you press Ctrl+C
    app.run_polling()
