import random
from telebot import types
import helpers
user1 = {}

DEFAULT_BUTTONS = []


'''def create_keyboard(buttons, rowsWidth=3):
    keyboard = types.ReplyKeyboardMarkup(
        resize_keyboard=True, row_width=rowsWidth)

    for button in buttons + DEFAULT_BUTTONS:
        if type(button) is list:
            keyboard.add(*map(lambda x: types.KeyboardButton(x), button))
        else:
            keyboard.add(types.KeyboardButton(button))

    return keyboard

'''
def enter(bot, user, all_users, location):
    if not user["id"] in user1:
        user1[user["id"]] = {"action": "stay"}
    bm = bm_create(bot, user1, user)
    bot.send_message(user["id"], 'Вы зашли в лес', reply_markup=bm)
    user1[user["id"]] = {"action": "stay"}
    bm.keyboard = []


def leave(bot, user, all_users, location):
    pass


def message(bot, message, user, all_users, location):
    if not user["id"] in user1:
        user1[user["id"]] = {"action": "stay"}
    if message.text == "Залезть на дерево":
        climb(bot, user)
    elif message.text == "Гамать":
        play(bot, user)
    elif message.text == "Перестать гамать":
        stop(bot, user)
    elif message.text == "Спуститься вниз":
        down(bot, user)
    else:
        bm = bm_create(bot, user1, user)
        bot.send_message(user["id"], "Лес", reply_markup=bm)


def events(bot, all_users, location):
    pass


def bm_create(bot, user1, user):
    item1 = "Гамать"
    item2 = "Залезть на дерево"
    item3 = "Перестать гамать"
    item4 = "Спуститься вниз"
    if user1[user["id"]]["action"] == "play" or user1[user["id"]]["action"] == "play on tree":
        item1 = ''
    if user1[user["id"]]["action"] == "tree" or user1[user["id"]]["action"] == "play on tree":
        item2 = ''
    if user1[user["id"]]["action"] != "play" and user1[user["id"]]["action"] != "play on tree":
        item3 = ''
    if user1[user["id"]]["action"] != "tree" and user1[user["id"]]["action"] != "play on tree":
        item4 = ''
    return helpers.create_keyboard([[item1, item2, item3, item4]])


def climb(bot, user):
    if user1[user["id"]]["action"] == "stay":
        user1[user["id"]]["action"] = "tree"
        bm = bm_create(bot, user1, user)
        bot.send_message(user["id"], "Вы забрались на дерево.", reply_markup=bm)

        if random.randint(3, 7) == 5:
            user1[user["id"]]["action"] = "stay"
            bm = bm_create(bot, user1, user)
            bot.send_message(user["id"], "Пока вы взбирались на дерево, вы наступили не на ту ветку и упали.", reply_markup=bm)
            user["fun"] -= 10
            user1[user["id"]]["action"] = "stay"
            if user["fun"] < 0:
                user["fun"] = 0
    elif user1[user["id"]]["action"] == "play":

        user1[user["id"]]["action"] = "play on tree"
        bm = bm_create(bot, user1, user)
        bot.send_message(user["id"], "Вы забрались на дерево и продолжили гамать.", reply_markup=bm)
        if random.randint(5, 7) == 5:
            user1[user["id"]]["action"] = "play"
            bm = bm_create(bot, user1, user)
            bot.send_message(user["id"],
                             "Пока вы взбирались на дерево, вы наступили не на ту ветку и упали. Теперь вы гамаете на земле", reply_markup=bm)
            user["fun"] -= 10
            user["health"] -= 2
            if user["fun"] < 0:
                user["fun"] = 0
    elif user1[user["id"]]["action"] == "tree" or user1[user["id"]]["action"] == "play on tree":
        bm = bm_create(bot, user1, user)
        bot.send_message(user["id"], "Вы и так находитесь на дереве", reply_markup=bm)


def play(bot, user):
    if user1[user["id"]]["action"] == "tree" or user1[user["id"]]["action"] == "stay":
        if user1[user["id"]]["action"] == "stay":
            user1[user["id"]]["action"] = "play"
            bm = bm_create(bot, user1, user)
            bot.send_message(user["id"], "Теперь вы нагло гамаете на опушке леса", reply_markup=bm)

        elif user1[user["id"]]["action"] == "tree":
            user1[user["id"]]["action"] = "play on tree"
            bm = bm_create(bot, user1, user)
            bot.send_message(user["id"], "Теперь вы гамаете на дереве", reply_markup=bm)
            if random.randint(2, 7) == 5:
                user1[user["id"]]["action"] = "play"
                bm = bm_create(bot, user1, user)
                bot.send_message(user["id"],"Пока вы доставали телефон, вы не удержали равновесие и упали. Теперь вы гамаете возле дерева.",reply_markup=bm)
                user["health"] -= 2
                user["fun"] -= 30

                if user["fun"] < 0:
                    user["fun"] = 0


        user["fun"] += 10
        if user["fun"] > 100:
            user["fun"] = 100
        if user1[user["id"]]["action"] == "play":
            if random.randint(4, 7) == 5:
                if random.randint(0, 100) < user["reputation"]:
                    bm = bm_create(bot, user1, user)
                    bot.send_message(user["id"],
                                     "Вас спалила Ирина Николаевна за наглым гаманием, но пащадила и не отрезала уголок",
                                     reply_markup=bm)
                else:
                    bm = bm_create(bot, user1, user)
                    bot.send_message(user["id"], "Вас спалила Ирина Николаевна за наглым гаманием и отрезала уголок",
                                     reply_markup=bm)
                    user["corners"]+=1
                user["fun"] -= 50
                if user["fun"] < 0:
                    user["fun"] = 0

    else:
        bm = bm_create(bot, user1, user)
        bot.send_message(user["id"], "Вы и так гамаете", reply_markup=bm)


def stop(bot, user):
    if user1[user["id"]]["action"] == "play" or user1[user["id"]]["action"] == "play on tree":
        if user1[user["id"]]["action"] == "play":
            user1[user["id"]]["action"] = "stay"
            bm = bm_create(bot, user1, user)
            bot.send_message(user["id"], "В вас проснулась совесть и вы перестали гамать", reply_markup=bm)
        else:
            user1[user["id"]]["action"] = "tree"
            bm = bm_create(bot, user1, user)
            bot.send_message(user["id"], "Вы продолжили сидеть на дереве, но уже не гамая", reply_markup=bm)
    else:
        bm = bm_create(bot, user1, user)
        bot.send_message(user["id"], "Вы не можете перестать гамать если не гамаете", reply_markup=bm)


def down(bot, user):
    if user1[user["id"]]["action"] == "tree" or user1[user["id"]]["action"] == "play on tree":
        if user1[user["id"]]["action"] == "tree":
            user1[user["id"]]["action"] = "stay"
            bm = bm_create(bot, user1, user)
            bot.send_message(user["id"], "Вы спустились с дерева", reply_markup=bm)
        else:
            user1[user["id"]]["action"] = "play"
            bm = bm_create(bot, user1, user)
            bot.send_message(user["id"], "Вы продолжили гамать на земле", reply_markup=bm)
    else:
<<<<<<< HEAD
        bm = bm_create(bot, user1, user)
        bot.send_message(user["id"], "Вы не на дереве!", reply_markup=bm)
=======
        bot.send_message(user["id"], "Вы не на дереве!")

def reset(user, location):
    pass
>>>>>>> origin/main
