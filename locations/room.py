import random

def enter(bot, user, all_users):
    bot.send_message(user["id"], "Вы зашли в комнату")

def leave(bot, user, all_users):
    pass

def message(bot, message, user, all_users):
    if message.text == "search":
        you_found = {
            "печенье": random.randint(10, 20)
        }
        bot.send_message(user["id"], f"Вы собрали: {', '.join([' в размере '.join([key, str(value)+'шт']) for key, value in you_found.items()])}")
        return
    bot.send_message(user["id"], "Комната")

def events(bot, all_users):
    pass