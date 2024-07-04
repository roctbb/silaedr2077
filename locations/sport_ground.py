import random
from telebot import types

basemarkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
item1=types.KeyboardButton("Поиграть в волейбол")
item2=types.KeyboardButton("Поиграть в футбол")
basemarkup.add(item1, item2)

playmarkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
item1=types.KeyboardButton("Поиграть в волейбол")
item2=types.KeyboardButton("Поиграть в футбол")
playmarkup.add(item1, item2)
usersData = {}
def enter(bot, user, all_users, location):
    if user["id"] not in usersData:
        bot.send_message(user["id"], f"Приветствуем на спорт площадке!\n Сейчас здесь находится {len(all_users)} людей.", reply_markup=basemarkup)
    else:
        bot.send_message(user["id"], f"С возвращением\nИгроков в спорте: {len(all_users)}, удачной игры!", reply_markup=basemarkup)

def leave(bot, user, all_users, location):
    pass

def message(bot, message, user, all_users, location):
    bot.send_message(user["id"], "Спорт площадка")
    if message.text=="Поиграть в волейбол":
        bot.send_message(user["id"], "Вы начали играть в волейбольчик")
    if message.text=="Поиграть в футбол":
        bot.send_message(user["id"], "Вы начали играть в фут")
def events(bot, all_users, location):
    pass