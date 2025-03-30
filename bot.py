import telebot
import os

CHANNEL_NAME = '@'
API_TOKEN = ''
TEMP_DIR = "temp/"

bot = telebot.TeleBot(API_TOKEN, skip_pending=True)
message_states = {}
last_pressed_time = {}

os.makedirs(TEMP_DIR, exist_ok=True)