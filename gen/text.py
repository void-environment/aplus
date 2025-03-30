from bot import bot
from text import get_gpt_response

def generate_yandex_text(message, cleaned_text, reply_text):

    if len(cleaned_text) > 4000:
        bot.send_message(message.chat.id, f"Очень длинный запрос.")
        return

    user_id = message.from_user.id
    username = message.from_user.username
    

    bot.send_chat_action(chat_id=user_id, action='typing')

    response_text = get_gpt_response(cleaned_text, reply_text)
    if "В интернете есть много сайтов с информацией на эту тему" in response_text:
        bot.send_message(message.chat.id, "Я не могу ответить на это. Попробуй другой запрос")
        return
    
    
    if "К сожалению, я не могу" in response_text: 
        bot.send_message(message.chat.id, 
            "Для изображений добавь #арт:\nНапример:\n"\
            "<blockquote>#арт милый кот с бананом</blockquote>",
            parse_mode='HTML'
        )
        return
    
    if "нейросетью YandexART" in response_text: 
        bot.send_message(message.chat.id, 
            "Для изображений добавь #арт:\nНапример:\n"\
            "<blockquote>#арт милый кот с бананом</blockquote>",
            parse_mode='HTML'
        )
        return
    
    bot.send_message(message.chat.id, response_text, parse_mode='MARKDOWN')