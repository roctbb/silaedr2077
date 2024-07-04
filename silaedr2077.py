import telebot
from config import TOKEN
import random
from locations import room, street

bot = telebot.TeleBot(TOKEN)

users = {}
locations = {
    "room": {

    },
    "street": {

    }
}

modules = {
    "room": room,
    "street": street
}


def add_user(message):
    users[message.from_user.id] = {
        "id": message.from_user.id,
        "cookies": random.randint(10, 60),
        "food": random.randint(50, 100),
        "water": random.randint(50, 100),
        "corners": 4,
        "knowledge": 0,
        "health": random.randint(20, 30),
        "reputation": random.randint(30, 60),
        "fun": random.randint(80, 100),
        "inventory": ["laptop", "phone", "bottle", "badge"],
        "location": "room"
    }


def is_registered(message):
    return message.from_user.id in users


@bot.message_handler(content_types=['text'])
def process_message(message):
    if not is_registered(message):
        add_user(message)

    user = users[message.from_user.id]
    if message.text == "/stats":
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

        module = modules[user["location"]]
        all_users = list(
            filter(lambda x: x["location"] == user["location"], users.values()))
        location = locations[user["location"]]
        module.enter(bot, user, all_users, location)
    else:
        module = modules[user["location"]]
        all_users = list(
            filter(lambda x: x["location"] == user["location"], users.values()))
        location = locations[user["location"]]

        module.message(bot, message, user, all_users, location)


bot.polling(none_stop=True)
