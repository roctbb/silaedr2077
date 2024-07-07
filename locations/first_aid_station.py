from telebot.types import BotCommand
from telebot import TeleBot
import telebot
from telebot import types
import helpers
import random
import time


def enter(bot, user, all_users, location):
    basemarkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Выйти")
    item5 = types.KeyboardButton("лечиться")
    basemarkup.add(item1, item5)
    bot.send_photo(user["id"], open('assets/first_aid_station.png', 'rb'),
                   caption="Вы зашли в медпункт." + '\n' + "Здесь вы лечитесь каждые 5 минут на 10 хп.", reply_markup=basemarkup)


def leave(bot, user, all_users, location=None):
    bot.send_message(
        user["id"], "Вовзвращайтесь в медпункт, если потребуется!")


def events(bot, all_users, location=None):
    for user in all_users:
        print(user["id"])
        if user['health'] < user['max_health']:
            user['health'] += 10
            bot.send_message(user["id"], "Вы восстановили 10 здоровья ❤️‍🩹" +
                             '\n' + f"Ваше здоровье: {user['health']}/{user['max_health']}")


def heal(bot, user, location):
    if (location == 'first_aid_station'):
        time.sleep(1)
        location["usersData"][user["id"]]["wait"] = False
        user['health'] = user['max_health']
        bot.send_message(user["id"], "Вы восстановили здоровье ❤️‍🩹" +
                         '\n' + "Ваше здоровье: " + str(user['max_health']))

    else:
        bot.send_message(user["id"], "Вы не в медпункте")


def message(bot, message, user, all_users, location):
    # if message.text == "лечиться":
    #    heal(bot, user, user['location'])
    if message.text == "Выйти":
        helpers.move_player(bot, user, "choice")


def reset(user, location):
    pass
