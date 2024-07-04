def enter(bot, user, all_users, location):
    bot.send_message(user["id"], "Вы зашли на спорт пощадку")

def leave(bot, user, all_users, location):
    pass

def message(bot, message, user, all_users, location):
    bot.send_message(user["id"], "Спорт площадка")

def events(bot, all_users, location):
    pass