def enter(bot, user, all_users, location, previous_location=None):
    bot.send_message(user["id"], "Вы зашли в комнату")

def leave(bot, user, all_users, location):
    pass

def message(bot, message, user, all_users, location):
    bot.send_message(user["id"], "Комната")

def events(bot, all_users, location):
    pass