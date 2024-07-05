from telebot.types import BotCommand
from telebot import TeleBot
import telebot
from telebot import types


def enter(bot, user, all_users, location):
    basemarkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("/room")
    item2 = types.KeyboardButton("/basement")
    item3 = types.KeyboardButton("/balcony")
    item5 = types.KeyboardButton("лечиться")
    basemarkup.add(item1, item2, item3, item5)
    bot.send_message(user["id"], "Вы зашли в медпункт",
                     reply_markup=basemarkup)
    photo = open('assets/first_aid_station.png', 'rb')
    bot.send_photo(user['id'], photo)


def leave(bot, user, all_users, location=None):
    bot.send_message(
        user["id"], "Вовзвращайтесь в медпункт, если потребуется!")
