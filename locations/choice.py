from helpers import *
from storage import *

basemarkup = create_keyboard([["Подвал", "Улица"], ["3 этаж"], ["4 этаж"]])

outsidemarkup = create_keyboard([["Болото", "Лес", "Спорт площадка"]])

floor3markup = create_keyboard([["Отмена", "Столовая"], list(rooms[3])], rowsWidth=7)
floor4markup = create_keyboard([["Отмена"], list(rooms[4])], rowsWidth=7)

def enter(bot, user, all_users, location):
    location["usersData"][user["id"]] = {
        "stage": 0
    }
    bot.send_message(user["id"], "Выбери куда пойти", reply_markup=basemarkup)

def leave(bot, user, all_users, location=None):
    pass

def message(bot, message, user, all_users, location):
    if location["usersData"][user["id"]]["stage"] == 0:
        if message.text == "Подвал":
            move_player(bot, user, "basement")
        elif message.text == "Улица":
            bot.send_message(user["id"], "Выбери куда локацию", reply_markup=outsidemarkup)
            location["usersData"][user["id"]]["stage"] = 1
        elif message.text == "3 этаж":
            bot.send_message(user["id"], "Выбери номер комнаты/столовку", reply_markup=floor3markup)
            location["usersData"][user["id"]]["stage"] = 2
        elif message.text == "4 этаж":
            bot.send_message(user["id"], "Выбери номер комнаты", reply_markup=floor4markup)
            location["usersData"][user["id"]]["stage"] = 3
        else:
            bot.send_message(user["id"], "Пользуйся кнопками!")
    elif location["usersData"][user["id"]]["stage"] == 1:
        if message.text == "Болото":
            move_player(bot, user, "swamp")
        elif message.text == "Лес":
            move_player(bot, user, "forest")
        elif message.text == "Спорт площадка":
            move_player(bot, user, "sport_ground")
        else:
            bot.send_message(user["id"], "Пользуйся кнопками!")
    elif location["usersData"][user["id"]]["stage"] == 2:
        if message.text == "Отмена":
            bot.send_message(user["id"], "Выбери куда пойти", reply_markup=basemarkup)
            location["usersData"][user["id"]]["stage"] = 0
        elif message.text == "Столовая":
            move_player(bot, user, "eatery")
        elif message.text.isdigit():
            if int(message.text) in rooms[3]:
                if user["id"] in locations["room"]["usersData"].keys():
                    locations["room"]["usersData"][user["id"]]["room"] = int(message.text)
                else:
                    locations["room"]["usersData"][user["id"]] = {
                        "room": int(message.text)
                    }
                move_player(bot, user, "room")
        else:
            bot.send_message(user["id"], "Пользуйся кнопками!")
    else:
        if message.text == "Отмена":
            bot.send_message(user["id"], "Выбери куда пойти", reply_markup=basemarkup)
            location["usersData"][user["id"]]["stage"] = 0
        elif message.text.isdigit():
            if int(message.text) in rooms[4]:
                if user["id"] in locations["room"]["usersData"].keys():
                    locations["room"]["usersData"][user["id"]]["room"] = int(message.text)
                else:
                    locations["room"]["usersData"][user["id"]] = {
                        "room": int(message.text)
                    }
                move_player(bot, user, "room")
        else:
            bot.send_message(user["id"], "Пользуйся кнопками!")


def events(bot, all_users):
    pass
