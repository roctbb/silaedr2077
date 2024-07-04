from telebot import types
import random
import time

basemarkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
item1=types.KeyboardButton("Покер")
item2=types.KeyboardButton("Пинг-понг")
basemarkup.add(item1, item2)


exitmarkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
item1=types.KeyboardButton("Выйти")
exitmarkup.add(item1)

choicemarkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
item1=types.KeyboardButton("Да")
item2=types.KeyboardButton("Нет")
choicemarkup.add(item1, item2)

tennisgamemarkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
item1=types.KeyboardButton("Слева")
item2=types.KeyboardButton("Спереди")
item3=types.KeyboardButton("Справа")
tennisgamemarkup.add(item1, item2, item3)

usersData = {}
locationImages = {
    0 : open("assets/basement.png"), 
    1 : open("assets/ping-pong.png"), 
    2 : open("assets/ping-pong.png"), 
    3 : open("assets/ping-pong.png"), 
    4 : open("assets/ping-pong.png"), 
    5 : open("assets/ping-pong.png"), 
    6 : open("assets/shop.png"), 
}

def enter(bot, user, all_users, location=None):
    if user["id"] not in usersData:
        bot.send_message(user["id"], f"Вижу ты тут впервые, ну чтож, думаю сам разберешся)\nСейчас здесь тусуется {len(all_users)} игроков", reply_markup=basemarkup)
    else:
        bot.send_message(user["id"], f"Снова привет братан)\nИгроков в подвале: {len(all_users)}", reply_markup=basemarkup)
    
    usersData[user["id"]] = {
        "playtennisConnection" : None, 
        "stage" : 0, 
        "shieldChoice" : [], 
        "attackChoice" : 0, 
        "turn" : -1, 
        "score" : [0, 0],
        "wait" : False 
    }
    
    

def leave(bot, user, all_users, location=None):
    bot.send_message(user["id"], "Ты вышел из подвала :(")

def checkShielder(bot, message, user, all_users):
    if usersData[usersData[user["id"]]["playtennisConnection"]["id"]]["attackChoice"] in usersData[user["id"]]["shieldChoice"]:
        score = [usersData[user["id"]]["score"][0], usersData[user["id"]]["score"][1]]
        bot.send_message(user["id"], f"Ты успешно отбил удар\nСчет {score[0]}:{score[1]}\nТеперь ты атакуешь", reply_markup=tennisgamemarkup)
        bot.send_message(usersData[user["id"]]["playtennisConnection"]["id"], f"Противник отбил твой удар\nсчет {score[1]}:{score[0]}\nТеперь ты защищаешь", reply_markup=tennisgamemarkup)
        usersData[usersData[user["id"]]["playtennisConnection"]["id"]]["stage"] = 4
    else:
        if usersData[user["id"]]["score"][1] + 1 == 5:
            score = [usersData[user["id"]]["score"][0], usersData[user["id"]]["score"][1]]
            bot.send_message(user["id"], f"Ты проиграл\nСчет {score[0]}:{score[1]+1}", reply_markup=basemarkup)
            bot.send_message(usersData[user["id"]]["playtennisConnection"]["id"], f"Ты победил!\nCчет {score[1]+1}:{score[0]}", reply_markup=basemarkup)
            usersData[user["id"]]["stage"] = 0
            usersData[usersData[user["id"]]["playtennisConnection"]["id"]]["stage"] = 0
            usersData[user["id"]]["score"] = [0, 0]
            usersData[usersData[user["id"]]["playtennisConnection"]["id"]]["score"] = [0, 0]
            usersData[user["id"]]["shieldChoice"] = []
            usersData[usersData[user["id"]]["playtennisConnection"]["id"]]["shieldChoice"] = []
            usersData[usersData[user["id"]]["playtennisConnection"]["id"]]["playtennisConnection"] = None
            usersData[user["id"]]["playtennisConnection"] = None
        else:
            usersData[user["id"]]["score"][1] += 1
            score = [usersData[user["id"]]["score"][0], usersData[user["id"]]["score"][1]]
            usersData[usersData[user["id"]]["playtennisConnection"]["id"]]["score"][0] += 1
            bot.send_message(user["id"], f"Тебе забили\nСчет {score[0]}:{score[1]}\nТеперь ты атакуешь", reply_markup=tennisgamemarkup)
            bot.send_message(usersData[user["id"]]["playtennisConnection"]["id"], f"Ты забил\nСчет {score[1]}:{score[0]}\nТеперь ты защищаешь", reply_markup=tennisgamemarkup)
            usersData[usersData[user["id"]]["playtennisConnection"]["id"]]["stage"] = 4

def checkAttacker(bot, message, user, all_users, location=None):
    if usersData[user["id"]]["attackChoice"] in usersData[usersData[user["id"]]["playtennisConnection"]["id"]]["shieldChoice"]:
        score = [usersData[user["id"]]["score"][0], usersData[user["id"]]["score"][1]]
        bot.send_message(user["id"], f"Противник отбил твой удар\nСчет {score[0]}:{score[1]}\nТеперь ты защищаешься", reply_markup=tennisgamemarkup)
        bot.send_message(usersData[user["id"]]["playtennisConnection"]["id"], f"Ты успешно отбил удар\nСчет {score[1]}:{score[0]}\nТеперь ты атакуешь", reply_markup=tennisgamemarkup)
        usersData[usersData[user["id"]]["playtennisConnection"]["id"]]["stage"] = 4
    else:
        if usersData[user["id"]]["score"][0] + 1 == 5:
            score = [usersData[user["id"]]["score"][0], usersData[user["id"]]["score"][1]]
            bot.send_message(user["id"], f"Ты победил!\nСчет {score[0]+1}:{score[1]}", reply_markup=basemarkup)
            bot.send_message(usersData[user["id"]]["playtennisConnection"]["id"], f"Ты проиграл\nСчет {score[1]}:{score[0]+1}", reply_markup=basemarkup)
            usersData[user["id"]]["stage"] = 0
            usersData[usersData[user["id"]]["playtennisConnection"]["id"]]["stage"] = 0
            usersData[user["id"]]["score"] = [0, 0]
            usersData[usersData[user["id"]]["playtennisConnection"]["id"]]["score"] = [0, 0]
            usersData[user["id"]]["shieldChoice"] = []
            usersData[usersData[user["id"]]["playtennisConnection"]["id"]]["shieldChoice"] = []
            usersData[usersData[user["id"]]["playtennisConnection"]["id"]]["playtennisConnection"] = None
            usersData[user["id"]]["playtennisConnection"] = None
        else:
            usersData[user["id"]]["score"][0] += 1
            score = [usersData[user["id"]]["score"][0], usersData[user["id"]]["score"][1]]
            usersData[usersData[user["id"]]["playtennisConnection"]["id"]]["score"][1] += 1
            bot.send_message(user["id"], f"Ты попал!\nСчет {score[0]}:{score[1]}\nТеперь ты защищаешь", reply_markup=tennisgamemarkup)
            bot.send_message(usersData[user["id"]]["playtennisConnection"]["id"], f"Тебе забили\nСчет {score[1]}:{score[0]}\nТеперь ты атакуешь", reply_markup=tennisgamemarkup)
            usersData[usersData[user["id"]]["playtennisConnection"]["id"]]["stage"] = 4

def message(bot, message, user, all_users, location=None):
    # pingpongMainGame
    # waiting
    if not usersData[user["id"]]["wait"]:
        usersData[user["id"]]["wait"] = True
        if usersData[user["id"]]["stage"] == 5:
            if message.text == "Выйти":
                usersData[user["id"]]["stage"] = 0
                usersData[usersData[user["id"]]["playtennisConnection"]["id"]]["stage"] = 0
                usersData[user["id"]]["score"] = [0, 0]
                usersData[usersData[user["id"]]["playtennisConnection"]["id"]]["score"] = [0, 0]
                usersData[user["id"]]["shieldChoice"] = []
                usersData[usersData[user["id"]]["playtennisConnection"]["id"]]["shieldChoice"] = []
                bot.send_message(user["id"], "Игра окончена", reply_markup=basemarkup)
                bot.send_message(usersData[user["id"]]["playtennisConnection"]["id"], "Противник вышел, игра окончена", reply_markup=basemarkup)
                usersData[usersData[user["id"]]["playtennisConnection"]["id"]]["playtennisConnection"] = None
                usersData[user["id"]]["playtennisConnection"] = None
            else:
                bot.send_message(user["id"], "Ожидай оппонента или нажми 'Выйти'")
        # choosing
        if usersData[user["id"]]["stage"] == 4:
            if usersData[user["id"]]["turn"] == -1:
                if len(usersData[user["id"]]["shieldChoice"]) == 2:
                    usersData[user["id"]]["shieldChoice"] = []
                if message.text == "Слева":
                    usersData[user["id"]]["shieldChoice"].append(0)
                elif message.text == "Спереди":
                    usersData[user["id"]]["shieldChoice"].append(1)
                elif message.text == "Справа":
                    usersData[user["id"]]["shieldChoice"].append(2)
                if len(usersData[user["id"]]["shieldChoice"]) == 2:
                    if usersData[usersData[user["id"]]["playtennisConnection"]["id"]]["stage"] == 4:
                        bot.send_message(user["id"], "Ты сделал выбор, ожидай противника...", reply_markup=exitmarkup)
                        usersData[user["id"]]["stage"] = 5
                        usersData[user["id"]]["turn"] *= -1
                    else:
                        checkShielder(bot, message, user, all_users)
                        usersData[user["id"]]["turn"] *= -1
                else:
                    bot.send_message(user["id"], "Выбери еще одно место для защиты")
            else:
                if message.text == "Слева":
                    usersData[user["id"]]["attackChoice"] = 0
                elif message.text == "Спереди":
                    usersData[user["id"]]["attackChoice"] = 1
                elif message.text == "Справа":
                    usersData[user["id"]]["attackChoice"] = 2
                
                if usersData[usersData[user["id"]]["playtennisConnection"]["id"]]["stage"] == 4:
                        bot.send_message(user["id"], "Ты сделал выбор, ожидай противника...", reply_markup=exitmarkup)
                        usersData[user["id"]]["stage"] = 5
                        usersData[user["id"]]["turn"] *= -1
                else:
                    checkAttacker(bot, message, user, all_users)
                    usersData[user["id"]]["turn"] *= -1

        
        # cansel if u are tennis host + waiting for opponent to confirm -----------------------------
        elif usersData[user["id"]]["stage"] == 3:
            if message.text == "Выйти":
                usersData[user["id"]]["stage"] = 0
                bot.send_message(user["id"], "Вы вышли в главное меню", reply_markup=basemarkup)
                usersData[usersData[user["id"]]["playtennisConnection"]["id"]]["stage"] = 0
                bot.send_message(usersData[user["id"]]["playtennisConnection"]["id"], f"Ваш оппонент отозвал предложение", reply_markup=basemarkup)
                usersData[usersData[user["id"]]["playtennisConnection"]["id"]]["playtennisConnection"] = None
                usersData[user["id"]]["playtennisConnection"] = None
            else:
                bot.send_message(user["id"], "Вы можете только выйти(нажмите кнопку в меню)")
        # choice if someone wants to play with u -----------------------------
        elif usersData[user["id"]]["stage"] == 2:
            if message.text == "Нет":
                bot.send_message(user["id"], "Окей, отмена", reply_markup=basemarkup)
                usersData[user["id"]]["stage"] = 0
                n = user["name"]
                bot.send_message(usersData[user["id"]]["playtennisConnection"]["id"], f"{n} отказался :(", reply_markup=basemarkup)
                usersData[usersData[user["id"]]["playtennisConnection"]["id"]]["stage"] = 0
                usersData[usersData[user["id"]]["playtennisConnection"]["id"]]["playtennisConnection"] = None
                usersData[user["id"]]["playtennisConnection"] = None
            else:
                bot.send_message(user["id"], "Начинаем игру!", reply_markup=tennisgamemarkup)
                usersData[user["id"]]["stage"] = 4
                bot.send_message(usersData[user["id"]]["playtennisConnection"]["id"], "Оппонент согласен, начинаем игру!", reply_markup=tennisgamemarkup)
                usersData[usersData[user["id"]]["playtennisConnection"]["id"]]["stage"] = 4
                
                # game starting
                
                usersData[user["id"]]["turn"] = random.choice([-1, 1])
                if usersData[user["id"]]["turn"] == 1:
                    bot.send_message(user["id"], "Ты атакуешь, выбери куда будешь бить")
                    bot.send_message(usersData[user["id"]]["playtennisConnection"]["id"], "Ты защищаешься, выбери что будешь защищать")
                else:
                    bot.send_message(user["id"], "Ты защищаешься, выбери что будешь защищать")
                    bot.send_message(usersData[user["id"]]["playtennisConnection"]["id"], "Ты атакуешь, выбери куда будешь бить")
                usersData[usersData[user["id"]]["playtennisConnection"]["id"]]["turn"] = usersData[user["id"]]["turn"]*-1
        # opponent choice -----------------------------
        elif usersData[user["id"]]["stage"] == 1:
            if message.text == "Отмена":
                usersData[user["id"]]["stage"] = 0
                bot.send_message(user["id"], "Окей, отмена", reply_markup=basemarkup)
            else:
                data = []
                for i in all_users:
                    if usersData[i["id"]]["stage"] in [0, 1] : data.append(i["name"])
                if message.text in data and message.text != user["name"]:
                    
                    for i in all_users:
                        if i["name"] == message.text:
                            usersData[user["id"]]["playtennisConnection"] = i
                            break
                    bot.send_message(user["id"], "Ожидаем подтверждение от " + message.text + "...", reply_markup=exitmarkup)
                    n = user["name"]
                    usersData[user["id"]]["stage"] = 3
                    bot.send_message(usersData[user["id"]]["playtennisConnection"]["id"], f"Игрок {n} предлагает вам сыграть в пинг-понг", reply_markup=choicemarkup)
                    usersData[usersData[user["id"]]["playtennisConnection"]["id"]]["playtennisConnection"] = user
                    usersData[usersData[user["id"]]["playtennisConnection"]["id"]]["stage"] = 2
                else:
                    markupPlayers = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    for i in all_users:
                        if i != user:
                            markupPlayers.add(i["name"])
                    markupPlayers.add("Отмена")
                    bot.send_message(user["id"], "Игрок не найден, возможно он уже вышел из подвала или играет с кем-то еще", reply_markup=markupPlayers)
                    
        # base menu -----------------------------
        elif usersData[user["id"]]["stage"] == 0:
            if message.text == "Покер":
                bot.send_message(user["id"], "выбран покер")
            if message.text == "Наст. Теннис":
                if len(all_users) > 1:
                    usersData[user["id"]]["playtennis"] = True
                    markupPlayers = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    for i in all_users:
                        if i != user:
                            markupPlayers.add(i["name"])
                    markupPlayers.add("Отмена")
                    usersData[user["id"]]["stage"] = 1
                    bot.send_message(user["id"], "Ты можеш сыграть, выбери игрока", reply_markup=markupPlayers)
                else:
                    bot.send_message(user["id"], "В подвале никого нет, попробуй позже")
        
        time.sleep(1)
        usersData[user["id"]]["wait"] = False
    else:
        bot.send_message(user["id"], "Не тыкай так часто :(")

def events(bot, all_users, location=None):
    pass
