import random
from telebot import types

basemarkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
item1=types.KeyboardButton("Поиграть в волейбол")
item2=types.KeyboardButton("Поиграть в футбол")
basemarkup.add(item1, item2)

playmarkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
item1=types.KeyboardButton("Серия пенальти(2 игрока)")
item2=types.KeyboardButton("Козел(2 игрока)")
item3=types.KeyboardButton("Футбол(4+ игроков, 2 команды)")
playmarkup.add(item1, item2, item3)
def enter(bot, user, all_users, location):
    if user["id"] not in location["players"]:
        bot.send_message(user["id"], f"Приветствуем на спорт площадке!\n Сейчас здесь находится {len(all_users)} людей.", reply_markup=basemarkup)
    else:
        bot.send_message(user["id"], f"С возвращением\nИгроков в спорте: {len(all_users)}, удачной игры!", reply_markup=basemarkup)

def leave(bot, user, all_users, location):
    pass

def message(bot, message, user, all_users, location):
    bot.send_message(user["id"], "Спорт площадка")
    if message.text=="Поиграть в волейбол":
        bot.send_message(user["id"], "Вы начали играть в волейбольчик", reply_markup=playmarkup)
    if message.text=="Поиграть в футбол":
        bot.send_message(user["id"], "Выберите режим игры", reply_markup=playmarkup)
        if message.text=="Серия пенальти(2 игрока)":
            bot.send_message(user["id"], "hiiiiii")
        if message.text=="Козел(2 игрока)":
            bot.send_message(user["id"], "Ни гатова(")
        if message.text=="Футбол(4+ игроков, 2 команды)":
            bot.send_message(user["id"], "Ни гатова(")
def events(bot, all_users, location):
    pass