import telebot
import requests

import markdown2
import re
import time
import datetime
current_time = datetime.datetime.now().time()

API_TOKEN = ''
bot = telebot.TeleBot(API_TOKEN)

headers = {
    'Authorization': 'Api-key ',
    'Content-Type': 'application/json'
}

def get_gpt_response(prompt):
    url = 'https://llm.api.cloud.yandex.net/foundationModels/v1/completion'
    payload = {
        "modelUri": "gpt:///yandexgpt-lite",
        "completionOptions": {
            "stream": False,
            "temperature": 0.6,
            "maxTokens": "500"
        },
        "messages": [
            {
                "role": "system",
                "text": ""
            },
            {
                "role": "user",
                "text": prompt + ''
            }
        ]
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        data = response.json()

        html = markdown2.markdown(data["result"]["alternatives"][0]["message"]["text"])
        plain_text = re.sub(r'<[^>]+>', '', html)

        return plain_text
    else:
        return "Ошибка при получении ответа от модели."

@bot.message_handler(func=lambda message: message.text)
def handle_message(message):

    response_text = get_gpt_response(message.text)

    if "В интернете есть много сайтов с информацией на эту тему" in response_text:
        bot.send_message(message.chat.id, f"Нахуя мне эта информация в {current_time}?")
    else:
        bot.send_message(message.chat.id, response_text)
bot.polling()
