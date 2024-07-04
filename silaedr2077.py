import telebot
from config import TOKEN
import random
from locations import room, street, balcony, basement

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

    }
}

modules = {
    "room": room,
    "balcony": balcony,
    "street": street,
    "basement": basement
}

paths = {
    "room": [],
    "street": [],
    "balcony": ["room"],
    "basement": []
}

def add_user(message):
    users[message.from_user.id] = {
        "id": message.from_user.id,
        "cookies": random.randint(10, 60),
        "food": random.randint(50, 100),
        "water": random.randint(50, 100),
        "corners": 4,
        "knowledge": 0,
        "reputation": random.randint(30, 60),
        "fun": random.randint(80, 100),
        "inventory": ["laptop", "phone", "bottle", "badge"],
        "location": "room"
    }


def is_registered(message):
    return message.from_user.id in users

def has_path(old_name, new_name):
    if not paths.get(old_name):
        return True

    return new_name in paths.get(old_name)


@bot.message_handler(content_types=['text'])
def process_message(message):
    if not is_registered(message):
        add_user(message)

    user = users[message.from_user.id]

    if message.text.startswith("/") and message.text.strip('/') in locations:
        old_location_name = user["location"]
        location_name = message.text.strip('/')

        if has_path(old_location_name, location_name):
            module = modules[user["location"]]
            all_users = list(filter(lambda x: x["location"] == user["location"], users.values()))
            old_location = locations[user["location"]]
            module.leave(bot, user, all_users, old_location)


            user["location"] = location_name

            module = modules[user["location"]]
            all_users = list(filter(lambda x: x["location"] == user["location"], users.values()))
            location = locations[user["location"]]
            module.enter(bot, user, all_users, location)
        else:
            bot.send_message(user["id"], "Not allowed")
    else:
        module = modules[user["location"]]
        all_users = list(filter(lambda x: x["location"] == user["location"], users.values()))
        location = locations[user["location"]]

        module.message(bot, message, user, all_users, location)


bot.polling(none_stop=True)
