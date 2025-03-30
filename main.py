from bot import bot

import handlers.start_handler
# import handlers.reset_handler
import handlers.text_handler
import handlers.voice_handler
# import handlers.business_handler

import sys, signal, time

def handle_exit(signal, frame):
    print("Bot stopped.")
    sys.exit(0)

def main():

    signal.signal(signal.SIGINT, handle_exit)

    while True:
        try:
            print("-=============================================-")
            print("Aplus start active")
            print("-=============================================-\n")
            bot.polling(non_stop=True) 
        except Exception as e:
            print("-=============================================-")
            print(f"Ошибка: {e}")
            print("Перезагрузка через 5 секунд...")
            print("-=============================================-\n")
            time.sleep(5) 

if __name__ == "__main__":
    main()