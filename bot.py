import os
import django
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from users.models import TelegramUser, TelegramConnectionToken, User  # Replace 'myapp' with your app name

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')  # Replace 'myproject' with your project name
django.setup()

# Synchronous function to generate a token for a user
def generate_token(email: str) -> tuple[str, str]:
    try:
        user = User.objects.get(email=email)
        # Delete any existing unused tokens for this user to avoid clutter
        TelegramConnectionToken.objects.filter(user=user, is_used=False).delete()
        token = TelegramConnectionToken.objects.create(user=user)
        return str(token.token), f"Token generated: {token.token}. Use /connect {token.token} to connect your account."
    except User.DoesNotExist:
        return None, "No user found with that email. Please provide a valid email registered in our system."

# Synchronous function to handle user connection logic
def connect_user(token: str, telegram_id: int) -> str:
    try:
        token_obj = TelegramConnectionToken.objects.get(token=token)
        if not token_obj.is_valid():
            return 'Invalid or expired token.'
        user = token_obj.user
        try:
            existing_telegram_user = user.telegram_user
            return 'This user is already connected to a Telegram account.'
        except TelegramUser.DoesNotExist:
            pass
        if TelegramUser.objects.filter(telegram_id=telegram_id).exists():
            return 'This Telegram account is already connected to another user.'
        TelegramUser.objects.create(user=user, telegram_id=telegram_id)
        token_obj.is_used = True
        token_obj.save()
        return 'Successfully connected your account!'
    except TelegramConnectionToken.DoesNotExist:
        return 'Invalid token.'

# Asynchronous handler for /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        'Hello! To connect your account:\n'
        '1. Use /token <your_email> to get a connection token.\n'
        '2. Use /connect <token> with the token you receive.'
    )

# Asynchronous handler for /token command
async def token(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) != 1:
        await update.message.reply_text('Please provide your email: /token <your_email>')
        return
    email = context.args[0]
    loop = asyncio.get_event_loop()
    token, message = await loop.run_in_executor(None, generate_token, email)
    await update.message.reply_text(message)

# Asynchronous handler for /connect command
async def connect(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) != 1:
        await update.message.reply_text('Please provide the token: /connect <token>')
        return
    token = context.args[0]
    telegram_id = update.message.from_user.id
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, connect_user, token, telegram_id)
    await update.message.reply_text(result)

if __name__ == '__main__':
    # Replace 'YOUR_BOT_TOKEN' with your actual Telegram bot token
    application = Application.builder().token('YOUR_BOT_TOKEN').build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('token', token))
    application.add_handler(CommandHandler('connect', connect))
    application.run_polling()