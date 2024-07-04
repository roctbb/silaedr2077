import telebot
from config import TOKEN
import random
from locations import room, street, balcony, basement, forest, swamp

bot = telebot.TeleBot(TOKEN)

users = {}
locations = {
    "room": {

    },
    "street": {

    },
    "balcony": {

    },
    "basement": {

    },
    "forest": {

    },
    "swamp":{

    }
}

modules = {
    "room": room,
    "balcony": balcony,
    "street": street,
    "basement": basement,
    "swamp": swamp, 
    "forest" : forest
}

def add_user(message):
    name = ""
    if message.from_user.first_name != None:
        name += message.from_user.first_name
    else:
        name += "Anonim"
    if message.from_user.last_name != None:
        name += " "
        name += message.from_user.last_name
    users[message.from_user.id] = {
        "id": message.from_user.id,
        "name": name,
        "cookies": random.randint(10, 60),
        "food": random.randint(50, 100),
        "water": random.randint(50, 100),
        "corners": 4,
        "knowledge": 0,
        "reputation": random.randint(30, 60),
        "fun": random.randint(80, 100),
        "inventory": ["laptop", "phone", "bottle", "badge"],
        "location": "room",
    }


def is_registered(message):
    return message.from_user.id in users

@bot.message_handler(content_types=['text'])
def process_message(message):
    if not is_registered(message):
        add_user(message)

    user = users[message.from_user.id]

    if message.text.startswith("/") and message.text.strip('/') in locations:
        module = modules[user["location"]]
        all_users = list(filter(lambda x: x["location"] == user["location"], users.values()))
        module.leave(bot, user, all_users)


        location_name = message.text.strip('/')
        user["location"] = location_name

        module = modules[user["location"]]
        all_users = list(filter(lambda x: x["location"] == user["location"], users.values()))
        module.enter(bot, user, all_users)
    else:
        module = modules[user["location"]]
        all_users = list(filter(lambda x: x["location"] == user["location"], users.values()))

        module.message(bot, message, user, all_users)


bot.polling(none_stop=True)
