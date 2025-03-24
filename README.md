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
    git clone git@github.com:KorlanE/queue-for-housing.git
    ```
2. Navigate to the project directory:
    ```bash
    cd queue-for-housing
    ```
3. Install the dependencies:
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