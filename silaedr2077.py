import assets
import telebot
from config import TOKEN
import random
from locations import room, street, balcony, basement, forest, swamp, first_aid_station
from storage import *
from helpers import *

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(content_types=['text'])
def process_message(message):
    if not is_registered(message):
        add_user(message)

    user = users[message.from_user.id]

    if message.text == "/locations":
        bot.send_message(user["id"], ', '.join(locations.keys()))
    elif message.text == "лечиться":
        heal(bot, user, user['location'])
    elif message.text == "/stats":
        give_stats(user, bot)

    elif message.text.startswith("/") and message.text.strip('/') in locations:
        old_location_name = user["location"]
        location_name = message.text.strip('/')

        if has_path(old_location_name, location_name):
            module = get_module(user)
            all_users = get_neighbours(user)

            module.leave(bot, user, all_users, locations[user['location']])
            user["location"] = location_name

            module = get_module(user)
            all_users = get_neighbours(user)
            module.enter(bot, user, all_users,
                         locations[user['location']], assets)
    else:
        module = get_module(user)
        all_users = get_neighbours(user)

        module.message(bot, message, user, all_users,
                       locations[user['location']])


bot.polling(none_stop=True)
