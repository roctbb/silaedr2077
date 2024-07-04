from helpers import *

basemarkup = create_keyboard([["Поесть", "Попить", "Украсть печеньку"]])

def enter(bot, user, all_users, location):
    bot.send_message(user["id"], "Ты зашел в столовку", reply_markup=basemarkup)

def leave(bot, user, all_users, location):
    pass

def message(bot, message, user, all_users, location):
    pass


def events(bot, all_users, location):
    pass