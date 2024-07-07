import helpers
import random

basemarkup = helpers.create_keyboard([["Крикнуть", "Прыгнуть", "Выйти"]])

def enter(bot, user, all_users, location, previous_location=None):
    bot.send_message(user["id"], "Вы вышли на балкон", reply_markup=basemarkup)

def leave(bot, user, all_users, location=None):
    pass
    #bot.send_message(user["id"], "Вы ушли с балкона")

def message(bot, message, user, all_users, location=None):
    if message.text.startswith("Выйти"):
        helpers.move_player(bot, user, "room")
    if message.text.startswith("Крикнуть"):
        msg = bot.send_message(user['id'], "Что вы хотите крикнуть?")
        bot.register_next_step_handler(msg, shouter)
    if message.text.startswith("Прыгнуть"):
        jump(bot, user)

def events(bot, all_users, location):
    pass

def shouter(message):
    shout(helpers.get_bot(), "Кто-то крикнул:\n" + message.text)

def shout(bot, message):
    for user in helpers.get_all_users():
        if user["location"] != "basement":
            bot.send_message(user["id"], message)

def jump(bot, user):
    bot.send_photo(user["id"], open("assets/balcony/backrooms/base.jpg", 'rb'), caption="Вы спрыгнули с балкона и провалились в backrooms...")
    helpers.move_player(bot, user, "first_aid_station")

def reset(user, location):
    pass