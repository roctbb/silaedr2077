def enter(bot, user, all_users, location, previous_loctaion=None):
    bot.send_message(user["id"], "Вы вышли на улицу")

def leave(bot, user, all_users, location=None):
    pass

def message(bot, message, user, all_users, location=None):
    bot.send_message(user["id"], "Улица")

def events(bot, all_users, location=None):
    pass