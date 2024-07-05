from storage import *
import random


def get_neighbours(user):
    return list(filter(lambda x: x["location"] == user["location"], users.values()))


def get_module(user):
    return modules[user["location"]]


def add_user(message):
    name = ""
    if message.from_user.first_name != None:
        name += message.from_user.first_name
    else:
        name += "Anonim"
    if message.from_user.last_name != None:
        name += " "
        name += message.from_user.last_name

    users[message.from_user.id] = {
        "id": message.from_user.id,
        "name": name,
        "cookies": random.randint(10, 60),
        "food": random.randint(50, 100),
        "water": random.randint(50, 100),
        "health": 20,
        "max_health": random.randint(20, 30),
        "corners": 4,
        "knowledge": 0,
        "reputation": random.randint(30, 60),
        "fun": random.randint(80, 100),
        "inventory": ["laptop", "phone", "bottle", "badge"],
        "location": "room"
    }


def has_path(old_name, new_name):
    if not paths.get(old_name):
        return True

    return new_name in paths.get(old_name)


def is_registered(message):
    return message.from_user.id in users


def give_stats(user, bot):
    text = ""
    text += "❤️ Здоровье - " + str(user['health']) + '/' + str(user['max_health']) + "\n" "💵 Деньги - " + str(user['cookies']) + "\n" + "🍟 Еда - " + str(user['food']) + "\n" + "💧 Вода - " + str(user['water']) + "\n" + "📃 Уголки - " + str(user['corners']) + "\n" + "😄 Веселье - " + str(
        user['fun']) + "\n" + "🏘 Локация - " + str(user['location']) + "\n" + "🫂 Репутация - " + str(user['reputation']) + "\n" + "🎒 инвентарь - " + ', '.join(user['inventory']) + "\n" + "👨‍🏫 знания - " + str(user['knowledge'])
    bot.send_message(user['id'], text)


def heal(bot, user, x):
    if (x == 'first_aid_station'):
        if (random.randint(0, 10000) == 2077):
            bot.send_message(user["id"], "Лечение провалилось, вы умерли 💔")
            user['health'] = 0
        else:
            user['health'] = user['max_health']
            bot.send_message(user["id"], "Вы восстановили здоровье ❤️‍🩹" +
                             '\n' + "Ваше здоровье: " + str(user['max_health']))

    else:
        bot.send_message(user["id"], "Вы не в медпункте")
