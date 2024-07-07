import random
import time
import helpers
from telebot import types

basemarkup = helpers.create_keyboard([["Волейбол", "Футбол"]])

playmarkup = helpers.create_keyboard([["Серия пенальти(2 игрока)", "Футбол(4, 6 или 8 игроков, 2 команды)"]])


def enter(bot, user, all_users, location):
    if user["id"] not in location["players"]:
        bot.send_photo(user["id"], open("assets/sport_ground/sport_ground.jpg", "rb"), caption="Приветствуем на спорт площадке!\n Сейчас здесь находится"+str({len(all_users)})+"людей.", reply_markup=basemarkup)  
    else:        
        bot.send_photo(user["id"], open("assets/sport_ground/sport_ground.jpg", "rb"), caption="С возвращением\nИгроков: "+str({len(all_users)})+", удачной игры!", reply_markup=basemarkup)
    location["locations"][user["id"]] = {
        "penaltyGameConnection": None, 
        "stage": 0, 
        "defChoice": [], 
        "attackChoice": 0, 
        "turn": -1, 
        "score": [0, 0],
        "wait": False, 
        "buyItem": [], 
        "sellItem": []
    }
def leave(bot, user, all_users, location):
    pass

def message(bot, message, user, all_users, location):
    bot.send_message(user["id"], "Спорт площадка")
    if message.text=="Поиграть в волейбол":
        bot.send_message(user["id"], "Вы начали играть в волейбольчик")
    if message.text=="Поиграть в футбол":
        bot.send_message(user["id"], "Выберите режим игры", reply_markup=playmarkup)
        if message.text=="Серия пенальти(2 игрока)":
            bot.send_message(user["id"], "Приветствуем в серии пенальти!")
        if message.text=="Футбол(4+ игроков, 2 команды)":
            bot.send_message(user["id"], "Ни гатова(")
def events(bot, all_users, location):
    pass

def reset(user, location):
    pass