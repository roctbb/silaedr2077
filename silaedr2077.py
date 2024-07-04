import telebot
from config import TOKEN
import random
from locations import room, street, balcony, basement, forest, swamp
from storage import *
from helpers import *

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(content_types=['text'])
def process_message(message):
    if not is_registered(message):
        add_user(message)

    user = users[message.from_user.id]

    if message.text.startswith("/") and message.text.strip('/') in locations:
        module = get_module(user)
        all_users = get_neighbours(user)

        module.leave(bot, user, all_users)


        location_name = message.text.strip('/')
        user["location"] = location_name

        module = get_module(user)
        all_users = get_neighbours(user)
        module.enter(bot, user, all_users)
    else:
        module = get_module(user)
        all_users = get_neighbours(user)

        module.message(bot, message, user, all_users)


bot.polling(none_stop=True)
