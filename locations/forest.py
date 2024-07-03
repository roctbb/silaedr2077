import random
def enter(bot, user, all_users, location):
    bot.send_message(user["id"], '''Вы зашли в лес
    /climb залезть на дерево
    /play начать гамать
    /stop перестать гамать''')
def leave(bot, user, all_users, location):
    pass

def message(bot, message, user, all_users, location):

    if message.text == "/climb":
        climb(bot, user)
    elif message.text == "/play":
        play(bot, user)
    else:
        bot.send_message(user["id"], "Лес")

def events(bot, all_users, location):
    pass
def climb(bot, user):
    bot.send_message(user["id"], "Вы забрались на дерево.")
    if random.randint(4,7)==5:
        bot.send_message(user["id"], "Пока вы взбирались на дерево, вы наступили не на ту ветку и упали.")
        user["fun"]-=10
        if user["fun"]<0:
            user["fun"]=0
def play(bot, user):
    bot.send_message(user["id"], "Теперь вы нагло гамаете на опушке леса")
    user["fun"]+=10
    if user["fun"]>100:
        user["fun"]=100
    if random.randint(4,7)==5:
        bot.send_message(user["id"], "Вас спалила Ирина Николаевна за наглым гаманием и збрала бейджик")
        user["fun"]-=50
        if user["fun"]<0:
            user["fun"]=0
def stop(bot, user):
    bot.send_message(user["id"], "В вас проснулась совести и вы перестали гамать")
