from bot import bot
from art import yandex_art_request

def generate_yandex_art(message, cleaned_text):

    if len(cleaned_text) > 450:
        bot.send_message(message.chat.id, f"Очень длинный запрос.")
        return

    prompt = cleaned_text

    try:
        bot.send_message(message.chat.id, f"Окей! 👌 <b>Генерирую для тебя:</b>\n\n<blockquote>{prompt}</blockquote>", parse_mode='HTML')
        generated_image_path = yandex_art_request(prompt) 

    except Exception as e:

        bot.send_message(message.chat.id, f"Не удалось сгенерировать")
        print(f"Ошибка art - {e}")
        return

    try:
        with open(generated_image_path, "rb") as image_file:
            bot.send_photo(message.chat.id, image_file)
    except Exception as e:
        bot.send_message(message.chat.id, f"Не удалось сгенерировать")
        print(f"Ошибка art - {e}")