# Вибираємо базовий образ
FROM python:3.11

# Встановлюємо залежності
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо скрипт
COPY telegram-forwarder.py telegram-forwarder.py

# Встановлюємо змінні середовища
ENV API_ID=XXXXXXX
ENV API_HASH=XXXXXXXXXXXXXXXXXXXXXXXXXXX
ENV PUBLIC_CHANNEL_USERNAME='@some_public_channel'
ENV PRIVATE_CHANNEL_ID=-10000000000
ENV SESSION_DIR=/app/session

# Запускаємо скрипт
CMD ["python", "telegram-forwarder.py"]
