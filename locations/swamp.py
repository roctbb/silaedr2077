def enter(bot, user, all_users):
    bot.send_message(user["id"], "Вы вошли на болото")

def leave(bot, user, all_users):
    pass

def message(bot, message, user, all_users):
    bot.send_message(user["id"], "Болото")

def events(bot, all_users):
    pass