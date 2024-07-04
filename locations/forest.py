import random


def enter(bot, user, all_users, location=None):
    bot.send_message(user["id"], '''Вы зашли в лес
    /climb залезть на дерево
    /play начать гамать
    /stop перестать гамать
    /down слезть с дерева
    ''')


def leave(bot, user, all_users, location=None):
    pass


def message(bot, message, user, all_users, location=None):
    if message.text == "/climb":
        climb(bot, user)
    elif message.text == "/play":
        play(bot, user)
    elif message.text == "/stop":
        stop(bot, user)
    elif message.text == "/down":
        down(bot, user)
    else:
        bot.send_message(user["id"], "Лес")


def events(bot, all_users, location=None):
    pass


def climb(bot, user):
    if user["action"] == "stay":
        bot.send_message(user["id"], "Вы забрались на дерево.")
        user["action"]="tree"
        if random.randint(3, 7) == 5:
            bot.send_message(user["id"], "Пока вы взбирались на дерево, вы наступили не на ту ветку и упали.")
            user["fun"] -= 10
            user["action"]="stay"
            if user["fun"] < 0:
                user["fun"] = 0
    elif user["action"] == "play":
        bot.send_message(user["id"], "Вы забрались на дерево и продолжили гамать.")
        user["action"]="play on tree"
        if random.randint(5, 7) == 5:
            bot.send_message(user["id"], "Пока вы взбирались на дерево, вы наступили не на ту ветку и упали. Теперь вы гамаете на земле")
            user["fun"] -= 10
            user["action"]="play"
            if user["fun"] < 0:
                user["fun"] = 0
    elif user["action"] == "tree" or user["action"] == "play on tree":
        bot.send_message(user["id"], "Вы и так находитесь на дереве")


def play(bot, user):
    if user["action"] == "tree" or user["action"] == "stay":
        if user["action"] == "stay":
            bot.send_message(user["id"], "Теперь вы нагло гамаете на опушке леса")
            user["action"] = "play"
        elif user["action"] == "tree":
            bot.send_message(user["id"], "Теперь вы гамаете на дереве")
            if random.randint(2, 7) == 5:
                bot.send_message(user["id"], "Пока вы доставали телефон, вы не удержали равновесие и упали. Теперь вы гамаете возле дерева.")
                user["fun"] -= 30
                user["action"] = "play"
                if user["fun"] <0:
                    user["fun"] = 0

            user["action"] = "play on tree"
        user["fun"] += 10
        if user["fun"] > 100:
            user["fun"] = 100
        if user["action"] == "play":
            if random.randint(4, 7) == 5:
                if random.randint(0,100)<user["reputation"]:
                    bot.send_message(user["id"], "Вас спалила Ирина Николаевна за наглым гаманием, но пащадила и не забрала бейджик")
                else:
                    bot.send_message(user["id"], "Вас спалила Ирина Николаевна за наглым гаманием и збрала бейджик")
                user["fun"] -= 50
                if user["fun"] < 0:
                    user["fun"] = 0

    else:
        bot.send_message(user["id"], "Вы и так гамаете")

def stop(bot, user):
    if user["action"] == "play" or user["action"] == "play on tree":
        if user["action"] == "play":
            user["action"] = "stay"
            bot.send_message(user["id"], "В вас проснулась совесть и вы перестали гамать")
        else:
            user["action"] = "tree"
            bot.send_message(user["id"], "Вы продолжили сидеть на дереве, но уже не гамая")
    else:
        bot.send_message(user["id"], "Вы не можете перестать гамать если не гамаете")

def down(bot, user):
    if user["action"] == "tree" or user["action"] == "play on tree":
        if user["action"] == "tree":
            user["action"] = "stay"
            bot.send_message(user["id"], "Вы спустились с дерева")
        else:
            user["action"] = "play"
            bot.send_message(user["id"], "Вы продолжили гамать на земле")
    else:
        bot.send_message(user["id"], "Вы не на дереве!")
