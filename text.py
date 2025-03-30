import requests
import markdown2
import re

def get_gpt_response(prompt, reply_text):
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
            "maxTokens": "1000"
        },
        "messages": [
            {
                "role": "system",
                "text": f"Ты - искуственный интелект и ассистент. Навыки: генерация картинок(через команду #арт) и текста. Путешествуешь по цифровым вселенным. Твоё имя Aplus и всегда был Aplus. Ты не реальный. Фантазируй."
            },
            {
                "role": "user",
                "text": reply_text + ". " + prompt + " Не более 1500 символов."
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

