def enter(bot, user, all_users, location):
    bot.send_message(user["id"], "Вы вошли на болото")

def leave(bot, user, all_users, location):
    pass

def message(bot, message, user, all_users, location):
    bot.send_message(user["id"], "Болото")

def events(bot, all_users, location):
    pass