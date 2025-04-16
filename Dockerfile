FROM python:3.12

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "main.py"]

# Expose the port the app runs on