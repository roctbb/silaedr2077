import telebot
from config import TOKEN
from storage import *
from helpers import *

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(content_types=['text'])
def process_message(message):
    if not is_registered(message):
        add_user(message)

    user = users[message.from_user.id]

    if message.text == "/locations":
        bot.send_message(user["id"], "/" + '\n/'.join(locations.keys()))
    elif message.text == "/stats":
        text = ""
        text += "Здоровье " + str(user['health']) + "\n" "Печеньки(валюта) " + str(user['cookies']) + "\n" + "Еда " + str(user['food']) + "\n" + "Вода " + str(user['water']) + "\n" + "Уголки " + str(user['corners']) + "\n" + "Веселье " + str(
            user['fun']) + "\n" + "Локация " + str(user['location']) + "\n" + "Репутация " + str(user['reputation']) + "\n" + "инвентарь " + ', '.join(user['inventory']) + "\n" + "знания " + str(user['knowledge'])
        bot.send_message(user['id'], text)

    elif message.text.startswith("/") and message.text.strip('/') in locations:
        move_player(bot, user, message.text.strip('/'))
    else:
        module = get_module(user)
        all_users = get_neighbours(user)

        module.message(bot, message, user, all_users, locations[user['location']])


bot.polling(none_stop=True)
