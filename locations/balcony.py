def enter(bot, user, all_users, location, previous_location=None):
    if location == "room":
        bot.send_message(user["id"], "Вы вышли на балкон")
    else:
        bot.send_message(user["id"], "На балкон можно выйти только из комнаты")

def leave(bot, user, all_users, location):
    pass

def message(bot, message, user, all_users, location):
    bot.send_message(user["id"], "Балкон")

def events(bot, all_users, location):
    pass