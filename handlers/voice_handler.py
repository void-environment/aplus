import os

from bot import bot
from utils.utils import clean_text, voice_to_text
from phrases.image import image_phrases
from gen.text import generate_yandex_text
from gen.image import generate_yandex_art

import speech_recognition as sr
from pydub import AudioSegment

@bot.message_handler(content_types=["voice"])
def handle_voice_message(message):

    if message.from_user.id != message.chat.id: return

    username = message.from_user.username

    text = voice_to_text(message)

    print("-=============================================-")
    print(f"{username} - Распознанный текст: {text}")
    cleaned_text = clean_text(text)
    print(f"{username} - Чистый текст: {cleaned_text}")
    print("-=============================================-\n")


    if text.split()[0].lower() in image_phrases:
        generate_yandex_art(message, cleaned_text)
        return

    reply_to_message = ''

    if message.reply_to_message and message.reply_to_message.text:
        reply_to_message = message.reply_to_message.text

    generate_yandex_text(message, cleaned_text, reply_to_message)
        