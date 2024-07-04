def enter(bot, user, all_users):
        bot.send_message(user["id"], "Вы вышли на балкон")
    
def leave(bot, user, all_users):
    pass

def message(bot, message, user, all_users):
    bot.send_message(user["id"], "Балкон")

def events(bot, all_users):
    pass