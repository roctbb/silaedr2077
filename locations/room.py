from helpers import *

usersData = {}

basemarkup = create_keyboard([["В разработке..."]])

def enter(bot, user, all_users, location):
    bot.send_message(user["id"], "Ты зашел в комнату [номер]", reply_markup=basemarkup)

def leave(bot, user, all_users, location):
    pass

def message(bot, message, user, all_users, location):
    pass


def events(bot, all_users, location):
    pass