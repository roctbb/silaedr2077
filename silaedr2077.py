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
    if message.text == "/locations":
        bot.send_message(user["id"], ', '.join(locations.keys()))
    elif message.text == "/stats":
        bot.send_message(user['id'], "Здоровье - " + str(user['health']))
        bot.send_message(user['id'], "Деньги - " + str(user['cookies']))
        bot.send_message(user['id'], "Еда - " + str(user['food']))
        bot.send_message(user['id'], "Вода - " + str(user['water']))
        bot.send_message(user['id'], "Уголки - " + str(user['corners']))
        bot.send_message(user['id'], "Веселье - " + str(user['fun']))
        bot.send_message(user['id'], "Локация - " + str(user['location']))
        bot.send_message(user['id'], "Репутация - " + str(user['reputation']))
        bot.send_message(user['id'], "инвентарь - " +
                         ', '.join(user['inventory']))
        bot.send_message(user['id'], "знания - " + str(user['knowledge']))

    elif message.text.startswith("/") and message.text.strip('/') in locations:
        location_name = message.text.strip('/')
        user["location"] = location_name

        module = get_module(user)
        all_users = get_neighbours(user)
        module.enter(bot, user, all_users, locations[user['location']])
    else:
        module = get_module(user)
        all_users = get_neighbours(user)

        module.message(bot, message, user, all_users,
                       locations[user['location']])


bot.polling(none_stop=True)
