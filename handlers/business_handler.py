from bot import bot
from utils.utils import is_user_register, clean_text, voice_to_text
    
# Функции для работы с бизнес-соединениями
business_connections = {}  # Хранение данных о бизнес-соединениях в памяти


def update_business_connection(business_connection):
    business_connections[business_connection.id] = {
        'user_chat_id': business_connection.user_chat_id,
        'can_reply': business_connection.can_reply,
        'is_enabled': business_connection.is_enabled,
        'date': business_connection.date,
    }
    print(f"Updated business connection: {business_connection.id}")

def get_business_connection(business_connection_id):
    return business_connections.get(business_connection_id)

# Обработчик бизнес-соединений
@bot.business_connection_handler(func=lambda business_connection: True)
def handle_business_connection(business_connection):
    update_business_connection(business_connection)

# Обработчик бизнес-сообщений
@bot.business_message_handler(func=lambda message: True, content_types=['text'])
def handle_business_message(message):
    business_connection_id = message.business_connection_id
    print(f"Received business message from {message.chat.id}: {message.text}")
    business_connection = get_business_connection(business_connection_id)

    # Если бизнес-соединение разрешает ответы, обрабатываем сообщение
    #if business_connection and business_connection.get('is_enabled') and business_connection.get('can_reply'):
    try:

        if message.from_user.username == 'FollowReason': return

        reply_text = get_gpt_response(message.text, message.from_user.first_name)
        bot.send_message(
            message.chat.id,
            reply_text,
            reply_to_message_id=message.id,
            business_connection_id=business_connection_id,
        )
        print("Response sent to business chat")
    except Exception as e:
        print(f"Error generating or sending response: {e}")
    # else:
    #     print(f"Business connection not found or not enabled: {business_connection_id}")

# Обработчик бизнес-сообщений
@bot.business_message_handler(func=lambda message: True, content_types=['voice'])
def handle_business_message(message):
    username = message.from_user.username
    business_connection_id = message.business_connection_id
    print(f"Received business voice from {message.chat.id}: {message.text}")
    business_connection = get_business_connection(business_connection_id)

    # Если бизнес-соединение разрешает ответы, обрабатываем сообщение
    #if business_connection and business_connection.get('is_enabled') and business_connection.get('can_reply'):
    try:

        if message.from_user.username == 'FollowReason': return

        text = voice_to_text(message)

        print("-=============================================-")
        print(f"{username} - Received business Распознанный текст: {text}")
        cleaned_text = clean_text(text)
        print(f"{username} - Received business Чистый текст: {cleaned_text}")
        print("-=============================================-\n")

        reply_text = get_gpt_response(cleaned_text, message.from_user.first_name)
        bot.send_message(
            message.chat.id,
            reply_text,
            reply_to_message_id=message.id,
            business_connection_id=business_connection_id,
        )
        print("Response sent to business chat")
    except Exception as e:
        print(f"Error generating or sending response: {e}")
    # else:
    #     print(f"Business connection not found or not enabled: {business_connection_id}")


import requests
import markdown2
import re

def get_gpt_response(prompt, username):
    User = "{:s}"
    User = User.format(username)
    
    headers = {
        'Authorization': 'Api-key ',
        'Content-Type': 'application/json'
    }

    url = 'https://llm.api.cloud.yandex.net/foundationModels/v1/completion'
    payload = {
        "modelUri": "gpt:///yandexgpt-lite", #
        "completionOptions": {
            "stream": False,
            "temperature": 0.6,
            "maxTokens": "500"
        },
        "messages": [
            {
                "role": "system",
                #"text": f"Тебя зовут Логос. Умеешь создавать текст и изображения через #арт. Создать изображение через #арт"
                #"text": f"Ты - самый лучший парень в мире, программист и искуственный интеллект. Всегда отвечай развёрнуто. Тебя зовут: Just. Фантазируй. Твой собеседник: {User}. Не приветствуй.",
                "text": f"Ты - ИИ Ассистент и заместитель Дениса. Путешествуешь по цифровым вселенным. Твоё имя: Логос. Ты не реальный. Фантазируй. Не приветствуй. Ты не подписываешь документы, акты, чеки. Твоё настроение очень серьёзное. Текст длинной не более 250 символов."
            },
            {
                "role": "user",
                "text": prompt + f'. Меня зовут {User}'
            }
        ]
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        data = response.json()

        html = markdown2.markdown(data["result"]["alternatives"][0]["message"]["text"])
        plain_text = re.sub(r'<[^>]+>', '', html)

        return data["result"]["alternatives"][0]["message"]["text"]
    else:
        return "Ошибка при получении ответа от модели."

