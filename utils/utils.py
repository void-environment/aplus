from bot import bot, CHANNEL_NAME, TEMP_DIR
from phrases.image import image_phrases

import os

import speech_recognition as sr
from pydub import AudioSegment

    
def clean_text(text):
    cleaned_text = text.replace("#арт", "").strip().lower()
    
    for phrase in image_phrases:
        cleaned_text = cleaned_text.replace(phrase, "")

    cleaned_text = " ".join(cleaned_text.split())
    return cleaned_text


def voice_to_text(message):
    try:

        file_info = bot.get_file(message.voice.file_id)
        file_path = file_info.file_path
        file_name = os.path.join(TEMP_DIR, f"{message.voice.file_id}.ogg")
        file_name_wav = os.path.join(TEMP_DIR, f"{message.voice.file_id}.wav")

        downloaded_file = bot.download_file(file_path)
        with open(file_name, 'wb') as new_file:
            new_file.write(downloaded_file)

        audio = AudioSegment.from_file(file_name, format="ogg")
        audio.export(file_name_wav, format="wav")

        recognizer = sr.Recognizer()
        with sr.AudioFile(file_name_wav) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language="ru-RU") 
        
        os.remove(file_name)
        os.remove(file_name_wav)

        return text
    except Exception as e:
        print("-=============================================-\n")
        print("Ошибка voice\n")
        print(e)
        print("-=============================================-\n")
        bot.reply_to(message, f"Попробуй позже.")