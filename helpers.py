from storage import *
import random
import telebot
from config import TOKEN
from telebot import types
import json

bot = telebot.TeleBot(TOKEN)


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

    users[str(message.from_user.id)] = {
        "id": str(message.from_user.id),
        "name": name,
        "cookies": random.randint(10, 60),
        "food": random.randint(50, 100),
        "water": random.randint(50, 100),
        "health": 20,
        "max_health": random.randint(20, 30),
        "corners": 4,
        "knowledge": 0,
        "reputation": random.randint(30, 80),
        "fun": random.randint(80, 100),
        "inventory": ["laptop", "phone", "bottle", f"badge - {name}"],
        "location": "room",
        "action": "stay"
    }


def is_registered(message):
    return str(message.from_user.id) in users


def get_all_users():
    return users.values()


def move_player(bot, user, location: str):
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
    keyboard = types.ReplyKeyboardMarkup(
        resize_keyboard=True, row_width=rowsWidth)

    for button in buttons + DEFAULT_BUTTONS:
        if type(button) is list:
            keyboard.add(*map(lambda x: types.KeyboardButton(x), button))
        else:
            keyboard.add(types.KeyboardButton(button))

    return keyboard


def get_bot():
    return bot


def give_stats(user, bot):
    text = ""
    text += "❤️ Здоровье - " + str(user['health']) + '/' + str(user['max_health']) + "\n" "🍪 Печеньки(валюта) - " + str(user['cookies']) + "\n" + "🍟 Еда - " + str(user['food']) + "\n" + "💧 Вода - " + str(user['water']) + "\n" + "📃 Уголки - " + str(user['corners']) + "\n" + "😄 Веселье - " + str(
        user['fun']) + "\n" + "🏘 Локация - " + str(user['location']) + "\n" + "🫂 Репутация - " + str(user['reputation']) + "\n" + "🎒 инвентарь - " + ', '.join(user['inventory']) + "\n" + "👨‍🏫 знания - " + str(user['knowledge'])
    bot.send_message(user['id'], text)


def save_data():
    with open('save.json', 'w', encoding='utf-8') as f:
        json.dump([users, locations], f, ensure_ascii=False, indent=4)
