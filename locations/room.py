import random

from helpers import *
from storage import rooms

basemarkup = create_keyboard([["Выйти на балкон", "Искать", "Выйти"]])

def enter(bot, user, all_users, location):
    if not location.get("roomData"):
        location["roomData"] = {
            room: True for room in [
                *list(rooms[3]), *list(rooms[4])
            ]
        }
    if not location["usersData"].get(user["id"]):
        bot.send_photo(user["id"], open("assets/room/scary_dark_room.jpg", "rb"),
                caption = "Ты зашел в комнату, но ты незнаешь в какую. В комнате темно и издалека доносится голос Инги Александровны. В конце концов ты выбежал от туда и решил выбрать комнату нормально")
        move_player(bot, user, "choice")
        return
    number = location["usersData"][user["id"]]["room"]
    bot.send_message(user["id"], f"Ты зашел в комнату {number}", reply_markup=basemarkup)

def leave(bot, user, all_users, location):
    pass

def message(bot, message, user, all_users, location):
    if message.text == "Выйти на балкон":
        move_player(bot, user, "balcony")
        return
    elif message.text == "Выйти":
        move_player(bot, user, "choice")
    elif message.text == "Искать":
        number = str(location["usersData"][user["id"]]["room"])
        if location["roomData"][number]:
            cookies = random.randint(20, 40)
            if number == "404":
                bot.send_message(user["id"], f"Ты нашел в комнате кучю печенек🍪", reply_markup = basemarkup)
                cookies += 100
            else:
                bot.send_message(user["id"], f"Ты нашел в комнате несколько печенек🍪", reply_markup = basemarkup)
            user["cookies"] += cookies
            location["roomData"][number] == False
        else:
            bot.send_message(user["id"], f"Ты не нашел печенек :(", reply_markup = basemarkup)
    else:
        bot.send_message(user["id"], "Используй кнопки!")




def events(bot, all_users, location):
    location["roomData"] = {
        room: True for room in [
            *list(rooms[3]), *list(rooms[4])
        ]
    }


def reset(user, location):
    pass