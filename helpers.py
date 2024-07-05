from storage import *
import random
from telebot import types


def get_neighbours(user):
    return list(filter(lambda x: x["location"] == user["location"], users.values()))


def get_module(user):
    from modules import available_modules
    return available_modules[user["location"]]


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
        "health": random.randint(20, 30),
        "corners": 4,
        "knowledge": 0,
        "reputation": random.randint(30, 80),
        "fun": random.randint(80, 100),
        "inventory": ["laptop", "phone", "bottle", "badge"],
        "location": "room",
        "action": "stay"
    }

def is_registered(message):
    return message.from_user.id in users

def get_all_users():
    return users.values()

def move_player(bot, user, location:str):
    if location == user["location"]:
        bot.send_message(user["id"], "Вы уже на этой локации")
    else:
        if location in locations.keys():
            module = get_module(user)
            all_users = get_neighbours(user)
            module.leave(bot, user, all_users, locations[user['location']])
            
            user["location"] = location
            module = get_module(user)
            all_users = get_neighbours(user)
            module.enter(bot, user, all_users, locations[user['location']])

def create_keyboard(buttons, rowsWidth=3):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=rowsWidth)

    for button in buttons + DEFAULT_BUTTONS:
        if type(button) is list:
            keyboard.add(*map(lambda x: types.KeyboardButton(x), button))
        else:
            keyboard.add(types.KeyboardButton(button))

    return keyboard
