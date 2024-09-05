#!/usr/bin/env python3

import os
import logging
from telethon import TelegramClient
import asyncio

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger()

# Отримання змінних середовища
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
public_channel_username = os.getenv('PUBLIC_CHANNEL_USERNAME')
private_channel_id = int(os.getenv('PRIVATE_CHANNEL_ID'))  # Переконуємося, що це int
session_dir = os.getenv('SESSION_DIR', './session')
message_id_file = os.path.join(session_dir, 'message_id.txt')

# Переконатися, що директорія для сесій існує
os.makedirs(session_dir, exist_ok=True)

# Ініціалізація клієнта Telegram
client = TelegramClient(os.path.join(session_dir, 'session'), api_id, api_hash)

# Текст, який потрібно додати до кінця кожного повідомлення
footer_text = "➡️ Підписатись @kievenergy"

# Функція для перевірки та пересилання повідомлень
async def check_and_forward():
    global last_message_id

    while True:
        try:
            logger.info("Checking for new messages...")
            # Отримуємо останні повідомлення з публічного каналу
            messages = await client.get_messages(public_channel_username, limit=1)
            if messages:
                latest_message = messages[0]
                logger.info(f"Found message ID {latest_message.id}")

                if latest_message.id != last_message_id:
                    # Отримуємо текст повідомлення без будь-якого очищення
                    message_text = latest_message.text
                    logger.info(f"Original message text: {message_text}")

                    # Додаємо текст до кінця повідомлення
                    final_text = f"{message_text}\n\n{footer_text}"
                    logger.info(f"Final message text: {final_text}")

                    # Пересилаємо текстове повідомлення в приватний канал
                    await client.send_message(private_channel_id, final_text)
                    logger.info(f"Message ID {latest_message.id} forwarded to private channel.")

                    # Оновлюємо ID останнього повідомлення
                    last_message_id = latest_message.id

                    # Зберігаємо ID останнього повідомлення
                    with open(message_id_file, 'w') as f:
                        f.write(str(last_message_id))
                    logger.info(f"Updated last_message_id to {last_message_id}")
                else:
                    logger.info("No new messages to forward.")
            else:
                logger.info("No new messages found.")
        except Exception as e:
            logger.error(f"Error occurred: {e}")

        # Затримка на 10 секунд
        await asyncio.sleep(10)

async def main():
    global last_message_id
    await client.start()
    logger.info("Client started.")

    # Завантаження останнього ID повідомлення
    if os.path.exists(message_id_file):
        with open(message_id_file, 'r') as f:
            last_message_id = int(f.read().strip())
        logger.info(f"Loaded last_message_id: {last_message_id}")
    else:
        last_message_id = None
        logger.info("No last_message_id file found, starting fresh.")

    await check_and_forward()

with client:
    client.loop.run_until_complete(main())
