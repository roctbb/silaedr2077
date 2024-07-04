def enter(bot, user, all_users, location, previous_loctaion=None):
    bot.send_message(user["id"], "Вы зашли в подвал")

def leave(bot, user, all_users, location):
    bot.send_message(user["id"], "Ты вышел из подвала:(")

def message(bot, message, user, all_users, location):
    bot.send_message(user["id"], "ага ты в подвале, да да")

def events(bot, all_users, location):
    pass