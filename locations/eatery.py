from helpers import *
from datetime import datetime
import random
from storage import *

basemarkup = create_keyboard([["Поесть", "Попить", "Украсть печеньку"], ["Выйти"]])

def enter(bot, user, all_users, location):
    if user["id"] not in location["usersData"].keys():
        location["usersData"][user["id"]] = {
            "stage": 0, 
            "visits": 1,
            "lastVisitDate": datetime.today().strftime('%Y-%m-%d')
        }
        bot.send_message(user["id"], "Ты зашел в столовку 1 раз из 3 сегодня", reply_markup=basemarkup)
    else:
        if location["usersData"][user["id"]]["lastVisitDate"]!=datetime.today().strftime('%Y-%m-%d'):
            location["usersData"][user["id"]]["visits"] = 1
        else:
            location["usersData"][user["id"]] = {
                "stage": 0, 
                "visits": location["usersData"][user["id"]]["visits"]+1,
                "lastVisitDate": datetime.today().strftime('%Y-%m-%d')
            }
        if location["usersData"][user["id"]]["visits"] == 4:
            bot.send_message(user["id"], "Ты уже приходил в столовку сегодня 3 раза, приходи завтра")
            move_player(bot, user, "choice")
        else:
            v = location["usersData"][user["id"]]["visits"]
            bot.send_message(user["id"], f"Ты зашел в столовку {v} раз из 3 сегодня", reply_markup=basemarkup)

def leave(bot, user, all_users, location):
    pass

def message(bot, message, user, all_users, location):
    if location["usersData"][user["id"]]["stage"] == 0:
        if message.text == "Поесть":
            if user["food"] < 90:
                rng = random.randint(20, 50)
                if rng > 100-user["food"]:
                    rng = 100-user["food"]
                user["food"] += rng
                bot.send_message(user["id"], f"Вы поели\n+{rng}🍗")
            else:
                bot.send_message(user["id"], "Вы не хотите есть")
        elif message.text == "Попить":
            if user["water"] < 90:
                rng = random.randint(20, 50)
                if rng > 100-user["water"]:
                    rng = 100-user["water"]
                user["water"] += rng
                bot.send_message(user["id"], f"Вы попили\n+{rng}💦")
            else:
                bot.send_message(user["id"], "Вы не хотите пить")
        elif message.text == "Украсть печеньку":
            rng = random.randint(1, 5)
            if random.randint(1, 10) == 1 or user["reputation"]<20:
                bot.send_message(user["id"], f"Вас спалили, забрали уголок :(\n-1 уголок🔼")
            else:
                user["cookies"] += rng
                if random.randint(1, 2) == 1:
                    bot.send_message(user["id"], f"Вы успешно украли печеньки\n+{rng} печенек🍪")
                else:
                    rng = random.randint(5, 15)
                    bot.send_message(user["id"], f"Вы успешно украли печеньки\nКажется кто-то заметил, но не стал рассказывать другим\n+{rng} печенек🍪\n-{rng} репутации⬇️")
                    user["reputation"] -= rng
        elif message.text == "Выйти":
            bot.send_message(user["id"], "Ты вышел из столовой")
            move_player(bot, user, "choice")
    users[user["id"]] = user
                    


def events(bot, all_users, location):
    pass