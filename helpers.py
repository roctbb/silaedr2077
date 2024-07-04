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