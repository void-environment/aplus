from bot import bot, user_service, message_states

@bot.message_handler(commands=['reset'])
def reset_image_generation(message):

    if message.from_user.id != message.chat.id: return

    try:
        bot.delete_message(message.chat.id, message_states[message.chat.id])
    except Exception as e:
        print("Сообщения не существует")

    bot.send_message(message.chat.id, f"Окей! 👌")
    user_service.removeFromGeneration(message.chat.id)