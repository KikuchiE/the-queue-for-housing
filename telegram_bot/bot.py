from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ConversationHandler, filters, ContextTypes
from dotenv import load_dotenv
import requests
import os

load_dotenv()

CHECK_QUEUE_URL = "http://localhost:8000/api/check-queue/"
API_URL = "http://localhost:8000/accounts/api/"
APP_URL = "http://localhost:8000/my-application/"
TOKEN = os.getenv('TELEGRAM_TOKEN')

# States for ConversationHandler
START, IIN, PASSWORD, IS_FOR_WARD, CURRENT_ADDRESS, IS_HOMELESS, RESIDENCE_CONDITION, MONTHLY_INCOME, LIVING_AREA, IS_VETERAN, IS_SINGLE_PARENT, HAS_DISABILITY, DISABILITY_DETAILS, ADULTS_COUNT, CHILDREN_COUNT, ELDERLY_COUNT, CREATE_APPLICATION = range(17)

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello!")
    return ConversationHandler.END

# Help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Available commands:\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/create_application - Create a new application\n"
        "/check_queue_position <IIN> - Check your queue position by IIN"
    )

# Check queue position command
async def check_queue_position(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Please provide an IIN. Usage: /check_queue_position <IIN>")
        return
    
    iin = context.args[0]
    if len(iin) != 12 or not iin.isdigit():
        await update.message.reply_text("Invalid IIN. It should be a 12-digit number.")
        return
    
    try:
        response = requests.post(f"{CHECK_QUEUE_URL}", json={"iin": iin})
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

# Create application conversation
async def start_create_application(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Please enter your IIN:")
    return IIN

async def get_iin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    iin = update.message.text
    if len(iin) != 12 or not iin.isdigit():
        await update.message.reply_text("Invalid IIN. It should be a 12-digit number. Please enter again:")
        return IIN
    context.user_data['iin'] = iin
    await update.message.reply_text("Please enter your password:")
    return PASSWORD

async def get_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['password'] = update.message.text
    iin = context.user_data['iin']
    password = context.user_data['password']
    response = requests.post(f"{API_URL}authenticate/", json={'iin': iin, 'password': password})
    if response.status_code == 200:
        await update.message.reply_text("Authentication successful. Let's proceed.")
        keyboard = [
            [InlineKeyboardButton("For myself", callback_data='no')],
            [InlineKeyboardButton("For ward", callback_data='yes')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Is this application for yourself or for a ward?", reply_markup=reply_markup)
        return IS_FOR_WARD
    else:
        await update.message.reply_text("Authentication failed. Please check your IIN and password.")
        return ConversationHandler.END

async def get_is_for_ward(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['is_for_ward'] = query.data == 'yes'
    await query.edit_message_text(text=f"Application is for {'ward' if query.data == 'yes' else 'myself'}")
    await query.message.reply_text("Please enter your current address:")
    return CURRENT_ADDRESS

async def get_current_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['current_address'] = update.message.text
    keyboard = [
        [InlineKeyboardButton("Yes", callback_data='yes')],
        [InlineKeyboardButton("No", callback_data='no')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Are you homeless?", reply_markup=reply_markup)
    return IS_HOMELESS

async def get_is_homeless(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['is_homeless'] = query.data == 'yes'
    await query.edit_message_text(text=f"Homeless: {'Yes' if query.data == 'yes' else 'No'}")
    keyboard = [
        [InlineKeyboardButton("Good", callback_data='GOOD')],
        [InlineKeyboardButton("Adequate", callback_data='ADEQUATE')],
        [InlineKeyboardButton("Poor", callback_data='POOR')],
        [InlineKeyboardButton("Unsafe", callback_data='UNSAFE')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text("What is the condition of your current residence?", reply_markup=reply_markup)
    return RESIDENCE_CONDITION

async def get_residence_condition(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['current_residence_condition'] = query.data
    await query.edit_message_text(text=f"Residence condition: {query.data}")
    await query.message.reply_text("Please enter your monthly income (in numbers, e.g., 100000):")
    return MONTHLY_INCOME

async def get_monthly_income(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        income = float(update.message.text)
        context.user_data['monthly_income'] = income
        await update.message.reply_text("Please enter your current living area (in square meters, e.g., 50):")
        return LIVING_AREA
    except ValueError:
        await update.message.reply_text("Invalid input. Please enter a number for monthly income:")
        return MONTHLY_INCOME

async def get_living_area(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        area = float(update.message.text)
        context.user_data['current_living_area'] = area
        keyboard = [
            [InlineKeyboardButton("Yes", callback_data='yes')],
            [InlineKeyboardButton("No", callback_data='no')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Are you a veteran?", reply_markup=reply_markup)
        return IS_VETERAN
    except ValueError:
        await update.message.reply_text("Invalid input. Please enter a number for living area:")
        return LIVING_AREA

async def get_is_veteran(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['is_veteran'] = query.data == 'yes'
    await query.edit_message_text(text=f"Veteran: {'Yes' if query.data == 'yes' else 'No'}")
    keyboard = [
        [InlineKeyboardButton("Yes", callback_data='yes')],
        [InlineKeyboardButton("No", callback_data='no')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text("Are you a single parent?", reply_markup=reply_markup)
    return IS_SINGLE_PARENT

async def get_is_single_parent(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['is_single_parent'] = query.data == 'yes'
    await query.edit_message_text(text=f"Single parent: {'Yes' if query.data == 'yes' else 'No'}")
    keyboard = [
        [InlineKeyboardButton("Yes", callback_data='yes')],
        [InlineKeyboardButton("No", callback_data='no')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text("Do you have a disability?", reply_markup=reply_markup)
    return HAS_DISABILITY

async def get_has_disability(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['has_disability'] = query.data == 'yes'
    await query.edit_message_text(text=f"Has disability: {'Yes' if query.data == 'yes' else 'No'}")
    if context.user_data['has_disability']:
        await query.message.reply_text("Please provide details about your disability:")
        return DISABILITY_DETAILS
    else:
        await query.message.reply_text("Please enter the number of adults in your household:")
        return ADULTS_COUNT

async def get_disability_details(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['disability_details'] = update.message.text
    await update.message.reply_text("Please enter the number of adults in your household:")
    return ADULTS_COUNT

async def get_adults_count(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        count = int(update.message.text)
        if count < 1:
            raise ValueError
        context.user_data['adults_count'] = count
        await update.message.reply_text("Please enter the number of children in your household:")
        return CHILDREN_COUNT
    except ValueError:
        await update.message.reply_text("Invalid input. Please enter a positive integer for adults count:")
        return ADULTS_COUNT

async def get_children_count(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        count = int(update.message.text)
        if count < 0:
            raise ValueError
        context.user_data['children_count'] = count
        await update.message.reply_text("Please enter the number of elderly in your household:")
        return ELDERLY_COUNT
    except ValueError:
        await update.message.reply_text("Invalid input. Please enter a non-negative integer for children count:")
        return CHILDREN_COUNT

async def get_elderly_count(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        count = int(update.message.text)
        if count < 0:
            raise ValueError
        context.user_data['elderly_count'] = count
        return await create_application(update, context)
    except ValueError:
        await update.message.reply_text("Invalid input. Please enter a non-negative integer for elderly count:")
        return ELDERLY_COUNT

async def create_application(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = {
        'iin': context.user_data['iin'],
        'password': context.user_data['password'],
        'category': 'SOCIAL_VULNERABLE',  # Default category, adjust as needed
        'is_for_ward': context.user_data['is_for_ward'],
        'current_address': context.user_data['current_address'],
        'is_homeless': context.user_data['is_homeless'],
        'current_residence_condition': context.user_data['current_residence_condition'],
        'monthly_income': context.user_data['monthly_income'],
        'current_living_area': context.user_data['current_living_area'],
        'is_veteran': context.user_data['is_veteran'],
        'is_single_parent': context.user_data['is_single_parent'],
        'has_disability': context.user_data['has_disability'],
        'disability_details': context.user_data.get('disability_details', ''),
        'adults_count': context.user_data['adults_count'],
        'children_count': context.user_data['children_count'],
        'elderly_count': context.user_data['elderly_count'],
    }
    response = requests.post(f"{API_URL}applications/", json=data)
    if response.status_code == 201:
        application_id = response.json()['id']
        context.user_data['application_id'] = application_id
        required_docs = ['ID_PROOF']
        if context.user_data['is_veteran']:
            required_docs.append('VETERAN_STATUS')
        if context.user_data['is_single_parent']:
            required_docs.append('SINGLE_PARENT_PROOF')
        doc_list = "\n".join(required_docs)
        await update.message.reply_text(
            f"Application created successfully. Your application ID is {application_id}.\n"
            f"Please upload the following documents:\n{doc_list}\n"
            f"Send each document with caption: /upload_doc {application_id} <document_type> <iin> <password>\n"
            f"For more details, visit: {APP_URL}{application_id}"
        )
        return ConversationHandler.END
    else:
        await update.message.reply_text("Failed to create application. Please try again.")
        return ConversationHandler.END

# Document upload handler
async def upload_doc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("\n\n")
    print(context.args)
    print(update.message.caption)
    print("\n\n")
    if update.message.caption:
        parts = update.message.caption.split()
        if len(parts) != 5 or parts[0] != '/upload_doc':
            await update.message.reply_text("Invalid command. Usage: /upload_doc <application_id> <document_type> <iin> <password>")
            return
        _, application_id, document_type, iin, password = parts
        file = update.message.document
        if file:
            file_path = await context.bot.get_file(file.file_id)
            byte_array = await file_path.download_as_bytearray()
            files = {'file': (file.file_name, byte_array)}
            data = {'iin': iin, 'password': password, 'document_type': document_type}
            response = requests.post(f"{API_URL}applications/{application_id}/documents/", files=files, data=data)
            if response.status_code == 201:
                await update.message.reply_text("Document uploaded successfully.")
            else:
                await update.message.reply_text(f"Failed to upload document: {response.json().get('error', 'Unknown error')}")
        else:
            await update.message.reply_text("No document found in the message.")
    else:
        await update.message.reply_text("Please send the document with the command in the caption.")

# Conversation handler
conv_handler = ConversationHandler(
    entry_points=[CommandHandler('create_application', start_create_application)],
    states={
        IIN: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_iin)],
        PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_password)],
        IS_FOR_WARD: [CallbackQueryHandler(get_is_for_ward)],
        CURRENT_ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_current_address)],
        IS_HOMELESS: [CallbackQueryHandler(get_is_homeless)],
        RESIDENCE_CONDITION: [CallbackQueryHandler(get_residence_condition)],
        MONTHLY_INCOME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_monthly_income)],
        LIVING_AREA: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_living_area)],
        IS_VETERAN: [CallbackQueryHandler(get_is_veteran)],
        IS_SINGLE_PARENT: [CallbackQueryHandler(get_is_single_parent)],
        HAS_DISABILITY: [CallbackQueryHandler(get_has_disability)],
        DISABILITY_DETAILS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_disability_details)],
        ADULTS_COUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_adults_count)],
        CHILDREN_COUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_children_count)],
        ELDERLY_COUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_elderly_count)],
        CREATE_APPLICATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, create_application)],
    },
    fallbacks=[],
    per_message=False,
)
# Main function
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('check_queue_position', check_queue_position))
    app.add_handler(conv_handler)
    app.add_handler(MessageHandler(filters.Document.ALL, upload_doc))
    app.run_polling()