from bot import bot
from utils.utils import clean_text

from gen.text import generate_yandex_text
from gen.image import generate_yandex_art

from phrases.image import image_phrases

@bot.message_handler()
def handle_message(message):

    if message.from_user.id != message.chat.id: return

    username = message.from_user.username

    cleaned_text = clean_text(message.text)

    print("-=============================================-")
    print(f"{username} - {message.text}")
    print(f"Чистый текст: {username} - {cleaned_text}")
    print("-=============================================-\n")

    
    if message.text.split()[0].lower() in image_phrases:
        generate_yandex_art(message, cleaned_text)
        return
    
    reply_to_message = ''

    if message.reply_to_message and message.reply_to_message.text:
        reply_to_message = message.reply_to_message.text

    try:
        generate_yandex_text(message, cleaned_text, reply_to_message)
    except Exception as e:

        bot.send_message(message.chat.id, f"Попробуй повторить попытку.")
        print(f"Ошибка текста - {e}")
        return