# The Queue for Housing (Очередь на жилье)


## Description
A housing waiting list system with automatic priority calculation. Automates the process of distributing state or municipal apartments.

## Key functions: 
-  ✅ Registration of housing applications with indication of living conditions
-  ✅ Automatic calculation of queue priority based on criteria (income, number of children, disability, etc.)
-  ✅ Checking availability of available housing
-  ✅ History of changes in application statuses
-  ✅ Automatic notifications about progress in the queue (optional)
-  ✅ The admin panel for data management,Issuing notifications about the need to update documents

## Technologies used:
- Django ORM for database management
- PostgreSQL for storing information
- Django REST API for interacting with external systems
- Celery + Redis for background priority processing
- Django Admin for working with the queue database
## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/KikuchiE/the-queue-for-housing.git
    ```
2. Navigate to the project directory:
    ```bash
    cd the-queue-for-housing
    ```
3. Create a virtual environment:
    ```bash
    python -m venv venv
    ```
4. Install the dependencies:
    ```bash
    python -m pip install -r requirements.txt
    ```

## Usage

1. Start the development server:
    ```bash
    python manage.py migrate
    python manage.py runserver
    ```
2. Open your browser and navigate to `http://localhost:8000`.

## Telegram bot

1. Create a bot using the BotFather on Telegram and get the token.
2. Add the token to your environment variables or directly in the code.
3. Create .env file in the telegram_bot directory and add the following variables:
    ```env
    TELEGRAM_BOT_TOKEN=your_token_here
    ```
4. Telegram Bot is located in telegram_bot directory.
    ```bash
    cd telegram_bot
    ```
5. Install the required libraries:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```
6. Run the bot script:
    ```bash

    python bot.py
    ```