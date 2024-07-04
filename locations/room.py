from storage import rooms, locations
import helpers
from modules import basement
from telebot import types
from datetime import datetime
import random

floorsmarkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
floorsmarkup.add(
    types.KeyboardButton("Подвал"),
    types.KeyboardButton("2 Этаж"),
    types.KeyboardButton("3 Этаж"),
    types.KeyboardButton("4 Этаж")
)
floormarkup3 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width = 7)
floormarkup3.add(
    *[str(room) for room in rooms[3]], "Выйти"
)
floormarkup4 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width = 7)
floormarkup4.add(
    *[str(room) for room in rooms[4]], "Выйти"
)

floormarkup2 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width = 7)
floormarkup2.add(
    "Попить", "Стащить печеньку", "Выйти"
)

cookies2floor = random.randint(5, 10)
start_time = datetime.now().time()

usersData = {}
def enter(bot, user, all_users, location, previous_location=None):
    bot.send_message(user["id"], "Выберете этаж на который вы хотите зайти", reply_markup = floorsmarkup)
    usersData[user["id"]] = {"floor": None, "room": None}

def leave(bot, user, all_users, location=None):
    if usersData.get(user["id"]):
        del usersData[user["id"]]

def message(bot, message, user, all_users, location=None):
    if usersData.get(user["id"]):
        if not usersData[user["id"]]["floor"]:
            match message.text:
                case "Подвал":
                    leave(bot, user, all_users, location)
                    user['location'] = "basement"
                    basement.enter(bot, user, all_users, locations["basement"])
                case "2 Этаж":
                    usersData[user["id"]]["floor"] = 2
                    bot.send_message(user["id"], "Выберете комнату в которую хотите пойти", reply_markup = floormarkup2)
                case "3 Этаж":
                    usersData[user["id"]]["floor"] = 3
                    bot.send_message(user["id"], "Выберете комнату в которую хотите пойти", reply_markup = floormarkup3)
                case "4 Этаж":
                    usersData[user["id"]]["floor"] = 4
                    bot.send_message(user["id"], "Выберете комнату в которую хотите пойти", reply_markup = floormarkup4)
        else:
            if message.text == "Выйти":
                usersData[user["id"]]["floor"] = None
                bot.send_message(user["id"], "Выберете этаж на который вы хотите зайти", reply_markup = floorsmarkup)
                usersData[user["id"]] = {"floor": None, "room": None}
                return
            match usersData[user["id"]]["floor"]:
                case 2:
                    match message.text:
                        case "Попить":
                            if user["water"] < 90:
                                bot.send_message(user["id"], "Вы попили воды")
                                user["water"] += 10
                            elif user["water"] < 100:
                                bot.send_message(user["id"], "Вы недопили воду")
                                user["water"] += 100 - user["water"]
                            else:
                                bot.send_message(user["id"], "Вы нехотите пить воду")
                        case "Стащить печеньку":
                            ...
                case 3:
                    ...
                case  4:
                    ...
        # you_found = {
        #     "печенье": random.randint(10, 20)
        # }
        # bot.send_message(user["id"], f"Вы собрали: {', '.join([' в размере '.join([key, str(value)+'шт']) for key, value in you_found.items()])}")
        # return


def events(bot, all_users, location=None):
    pass