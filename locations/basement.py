import random
import time

import helpers

from telebot import types

basemarkup = helpers.create_keyboard([["Магазин", "Пинг-понг", "Выйти"]])

exitmarkup = helpers.create_keyboard([["Выйти"]])

choicemarkup = helpers.create_keyboard([["Да", "Нет"]])

tennisgamemarkup = helpers.create_keyboard([["Слева", "Спереди", "Справа"]])

def enter(bot, user, all_users, location):
    if user["id"] not in location["usersData"]:
        bot.send_photo(user["id"], open("assets/basement/base.jpg", "rb"), caption=f"Вижу ты тут впервые, ну чтож, думаю сам разберешся)\nСейчас здесь тусуется {len(all_users)} игроков", reply_markup=basemarkup)
    else:
        bot.send_photo(user["id"], open("assets/basement/base.jpg", "rb"), caption=f"Снова привет братан)\nИгроков в подвале: {len(all_users)-1}", reply_markup=basemarkup)

    location["usersData"][user["id"]] = {
        "playtennisConnection" : None, 
        "stage" : 0, 
        "shieldChoice" : [], 
        "attackChoice" : 0, 
        "turn" : -1, 
        "score" : [0, 0],
        "wait" : False 
    }



def leave(bot, user, all_users, location=None):
    bot.send_photo(user["id"], open("assets/basement/exit.jpg", "rb"), caption="Ты вышел из подвала :(")

def checkShielder(bot, message, user, all_users, location):
    if location["usersData"][location["usersData"][user["id"]]["playtennisConnection"]["id"]]["attackChoice"] in location["usersData"][user["id"]]["shieldChoice"]:
        score = [location["usersData"][user["id"]]["score"][0], location["usersData"][user["id"]]["score"][1]]
        bot.send_message(user["id"], f"Ты успешно отбил удар\nСчет {score[0]}:{score[1]}\nТеперь ты атакуешь", reply_markup=tennisgamemarkup)
        bot.send_message(location["usersData"][user["id"]]["playtennisConnection"]["id"], f"Противник отбил твой удар\nсчет {score[1]}:{score[0]}\nТеперь ты защищаешь", reply_markup=tennisgamemarkup)
        location["usersData"][location["usersData"][user["id"]]["playtennisConnection"]["id"]]["stage"] = 4
    else:
        if location["usersData"][user["id"]]["score"][1] + 1 == 5:
            score = [location["usersData"][user["id"]]["score"][0], location["usersData"][user["id"]]["score"][1]]
            bot.send_photo(user["id"], open("assets/basement/ping-pong.jpg", "rb"), caption=f"Ты проиграл\nСчет {score[0]}:{score[1]+1}", reply_markup=basemarkup)
            bot.send_photo(location["usersData"][user["id"]]["playtennisConnection"]["id"], open("assets/basement/ping-pong.jpg", "rb"), caption=f"Ты победил!\nCчет {score[1]+1}:{score[0]}", reply_markup=basemarkup)
            location["usersData"][user["id"]]["stage"] = 0
            location["usersData"][location["usersData"][user["id"]]["playtennisConnection"]["id"]]["stage"] = 0
            location["usersData"][user["id"]]["score"] = [0, 0]
            location["usersData"][location["usersData"][user["id"]]["playtennisConnection"]["id"]]["score"] = [0, 0]
            location["usersData"][user["id"]]["shieldChoice"] = []
            location["usersData"][location["usersData"][user["id"]]["playtennisConnection"]["id"]]["shieldChoice"] = []
            location["usersData"][location["usersData"][user["id"]]["playtennisConnection"]["id"]]["playtennisConnection"] = None
            location["usersData"][user["id"]]["playtennisConnection"] = None
        else:
            location["usersData"][user["id"]]["score"][1] += 1
            score = [location["usersData"][user["id"]]["score"][0], location["usersData"][user["id"]]["score"][1]]
            location["usersData"][location["usersData"][user["id"]]["playtennisConnection"]["id"]]["score"][0] += 1
            bot.send_message(user["id"], f"Тебе забили\nСчет {score[0]}:{score[1]}\nТеперь ты атакуешь", reply_markup=tennisgamemarkup)
            bot.send_message(location["usersData"][user["id"]]["playtennisConnection"]["id"], f"Ты забил\nСчет {score[1]}:{score[0]}\nТеперь ты защищаешь", reply_markup=tennisgamemarkup)
            location["usersData"][location["usersData"][user["id"]]["playtennisConnection"]["id"]]["stage"] = 4

def checkAttacker(bot, message, user, all_users, location=None):
    if location["usersData"][user["id"]]["attackChoice"] in location["usersData"][location["usersData"][user["id"]]["playtennisConnection"]["id"]]["shieldChoice"]:
        score = [location["usersData"][user["id"]]["score"][0], location["usersData"][user["id"]]["score"][1]]
        bot.send_message(user["id"], f"Противник отбил твой удар\nСчет {score[0]}:{score[1]}\nТеперь ты защищаешься", reply_markup=tennisgamemarkup)
        bot.send_message(location["usersData"][user["id"]]["playtennisConnection"]["id"], f"Ты успешно отбил удар\nСчет {score[1]}:{score[0]}\nТеперь ты атакуешь", reply_markup=tennisgamemarkup)
        location["usersData"][location["usersData"][user["id"]]["playtennisConnection"]["id"]]["stage"] = 4
    else:
        if location["usersData"][user["id"]]["score"][0] + 1 == 5:
            score = [location["usersData"][user["id"]]["score"][0], location["usersData"][user["id"]]["score"][1]]
            bot.send_photo(user["id"], open("assets/basement/ping-pong.jpg", "rb"), caption=f"Ты победил!\nСчет {score[0]+1}:{score[1]}", reply_markup=basemarkup)
            bot.send_photo(location["usersData"][user["id"]]["playtennisConnection"]["id"], open("assets/basement/ping-pong.jpg", "rb"), caption=f"Ты проиграл\nСчет {score[1]}:{score[0]+1}", reply_markup=basemarkup)
            location["usersData"][user["id"]]["stage"] = 0
            location["usersData"][location["usersData"][user["id"]]["playtennisConnection"]["id"]]["stage"] = 0
            location["usersData"][user["id"]]["score"] = [0, 0]
            location["usersData"][location["usersData"][user["id"]]["playtennisConnection"]["id"]]["score"] = [0, 0]
            location["usersData"][user["id"]]["shieldChoice"] = []
            location["usersData"][location["usersData"][user["id"]]["playtennisConnection"]["id"]]["shieldChoice"] = []
            location["usersData"][location["usersData"][user["id"]]["playtennisConnection"]["id"]]["playtennisConnection"] = None
            location["usersData"][user["id"]]["playtennisConnection"] = None
        else:
            location["usersData"][user["id"]]["score"][0] += 1
            score = [location["usersData"][user["id"]]["score"][0], location["usersData"][user["id"]]["score"][1]]
            location["usersData"][location["usersData"][user["id"]]["playtennisConnection"]["id"]]["score"][1] += 1
            bot.send_message(user["id"], f"Ты попал!\nСчет {score[0]}:{score[1]}\nТеперь ты защищаешь", reply_markup=tennisgamemarkup)
            bot.send_message(location["usersData"][user["id"]]["playtennisConnection"]["id"], f"Тебе забили\nСчет {score[1]}:{score[0]}\nТеперь ты атакуешь", reply_markup=tennisgamemarkup)
            location["usersData"][location["usersData"][user["id"]]["playtennisConnection"]["id"]]["stage"] = 4

def message(bot, message, user, all_users, location=None):
    # pingpongMainGame
    # waiting
    if user["location"] == "basement":
        if not location["usersData"][user["id"]]["wait"]:
            location["usersData"][user["id"]]["wait"] = True
            if location["usersData"][user["id"]]["stage"] == 5:
                if message.text == "Выйти":
                    location["usersData"][user["id"]]["stage"] = 0
                    location["usersData"][location["usersData"][user["id"]]["playtennisConnection"]["id"]]["stage"] = 0
                    location["usersData"][user["id"]]["score"] = [0, 0]
                    location["usersData"][location["usersData"][user["id"]]["playtennisConnection"]["id"]]["score"] = [0, 0]
                    location["usersData"][user["id"]]["shieldChoice"] = []
                    location["usersData"][location["usersData"][user["id"]]["playtennisConnection"]["id"]]["shieldChoice"] = []
                    bot.send_photo(user["id"], open("assets/basement/base.jpg", "rb"), caption="Игра окончена", reply_markup=basemarkup)
                    bot.send_photo(location["usersData"][user["id"]]["playtennisConnection"]["id"], open("assets/basement/base.jpg", "rb"), caption="Противник вышел, игра окончена", reply_markup=basemarkup)
                    location["usersData"][location["usersData"][user["id"]]["playtennisConnection"]["id"]]["playtennisConnection"] = None
                    location["usersData"][user["id"]]["playtennisConnection"] = None
                else:
                    bot.send_photo(user["id"], open("assets/basement/ping-pong.jpg", "rb"), caption="Ожидай оппонента или нажми 'Выйти'")
            # choosing
            if location["usersData"][user["id"]]["stage"] == 4:
                if location["usersData"][user["id"]]["turn"] == -1:
                    if len(location["usersData"][user["id"]]["shieldChoice"]) == 2:
                        location["usersData"][user["id"]]["shieldChoice"] = []
                    if message.text == "Слева":
                        location["usersData"][user["id"]]["shieldChoice"].append(0)
                    elif message.text == "Спереди":
                        location["usersData"][user["id"]]["shieldChoice"].append(1)
                    elif message.text == "Справа":
                        location["usersData"][user["id"]]["shieldChoice"].append(2)
                    if len(location["usersData"][user["id"]]["shieldChoice"]) == 2:
                        if location["usersData"][location["usersData"][user["id"]]["playtennisConnection"]["id"]]["stage"] == 4:
                            bot.send_photo(user["id"], open("assets/basement/ping-pong.jpg", "rb"), caption="Ты сделал выбор, ожидай противника...", reply_markup=exitmarkup)
                            location["usersData"][user["id"]]["stage"] = 5
                            location["usersData"][user["id"]]["turn"] *= -1
                        else:
                            checkShielder(bot, message, user, all_users, location)
                            location["usersData"][user["id"]]["turn"] *= -1
                    else:
                        bot.send_message(user["id"], "Выбери еще одно место для защиты")
                else:
                    if message.text == "Слева":
                        location["usersData"][user["id"]]["attackChoice"] = 0
                    elif message.text == "Спереди":
                        location["usersData"][user["id"]]["attackChoice"] = 1
                    elif message.text == "Справа":
                        location["usersData"][user["id"]]["attackChoice"] = 2
                    
                    if location["usersData"][location["usersData"][user["id"]]["playtennisConnection"]["id"]]["stage"] == 4:
                            bot.send_photo(user["id"], open("assets/basement/ping-pong.jpg", "rb"), caption="Ты сделал выбор, ожидай противника...", reply_markup=exitmarkup)
                            location["usersData"][user["id"]]["stage"] = 5
                            location["usersData"][user["id"]]["turn"] *= -1
                    else:
                        checkAttacker(bot, message, user, all_users, location)
                        location["usersData"][user["id"]]["turn"] *= -1


            # cansel if u are tennis host + waiting for opponent to confirm -----------------------------
            elif location["usersData"][user["id"]]["stage"] == 3:
                if message.text == "Выйти":
                    location["usersData"][user["id"]]["stage"] = 0
                    bot.send_photo(user["id"], open("assets/basement/base.jpg", "rb"), caption="Вы вышли в главное меню", reply_markup=basemarkup)
                    location["usersData"][location["usersData"][user["id"]]["playtennisConnection"]["id"]]["stage"] = 0
                    bot.send_photo(location["usersData"][user["id"]]["playtennisConnection"]["id"], open("assets/basement/base.jpg", "rb"), caption=f"Ваш оппонент отозвал предложение", reply_markup=basemarkup)
                    location["usersData"][location["usersData"][user["id"]]["playtennisConnection"]["id"]]["playtennisConnection"] = None
                    location["usersData"][user["id"]]["playtennisConnection"] = None
                else:
                    bot.send_message(user["id"], "Вы можете только выйти(нажмите кнопку в меню)")
            # choice if someone wants to play with u -----------------------------
            elif location["usersData"][user["id"]]["stage"] == 2:
                if message.text == "Нет":
                    bot.send_photo(user["id"], open("assets/basement/base.jpg", "rb"), caption="Отмена", reply_markup=basemarkup)
                    location["usersData"][user["id"]]["stage"] = 0
                    n = user["name"]
                    bot.send_photo(location["usersData"][user["id"]]["playtennisConnection"]["id"], open("assets/basement/base.jpg", "rb"), caption=f"{n} отказался :(", reply_markup=basemarkup)
                    location["usersData"][location["usersData"][user["id"]]["playtennisConnection"]["id"]]["stage"] = 0
                    location["usersData"][location["usersData"][user["id"]]["playtennisConnection"]["id"]]["playtennisConnection"] = None
                    location["usersData"][user["id"]]["playtennisConnection"] = None
                else:
                    bot.send_photo(user["id"], open("assets/basement/ping-pong.jpg", "rb"), caption="Начинаем игру!", reply_markup=tennisgamemarkup)
                    location["usersData"][user["id"]]["stage"] = 4
                    bot.send_photo(location["usersData"][user["id"]]["playtennisConnection"]["id"], open("assets/basement/ping-pong.jpg", "rb"), caption="Оппонент согласен, начинаем игру!", reply_markup=tennisgamemarkup)
                    location["usersData"][location["usersData"][user["id"]]["playtennisConnection"]["id"]]["stage"] = 4

                    # game starting

                    location["usersData"][user["id"]]["turn"] = random.choice([-1, 1])
                    if location["usersData"][user["id"]]["turn"] == 1:
                        bot.send_message(user["id"], "Ты атакуешь, выбери куда будешь бить")
                        bot.send_message(location["usersData"][user["id"]]["playtennisConnection"]["id"], "Ты защищаешься, выбери что будешь защищать")
                    else:
                        bot.send_message(user["id"], "Ты защищаешься, выбери что будешь защищать")
                        bot.send_message(location["usersData"][user["id"]]["playtennisConnection"]["id"], "Ты атакуешь, выбери куда будешь бить")
                    location["usersData"][location["usersData"][user["id"]]["playtennisConnection"]["id"]]["turn"] = location["usersData"][user["id"]]["turn"]*-1
            # opponent choice -----------------------------
            elif location["usersData"][user["id"]]["stage"] == 1:
                if message.text == "Отмена":
                    location["usersData"][user["id"]]["stage"] = 0
                    bot.send_photo(user["id"], open("assets/basement/base.jpg", "rb"), caption="Отмена", reply_markup=basemarkup)
                else:
                    data = []
                    for i in all_users:
                        if location["usersData"][i["id"]]["stage"] in [0, 1] : data.append(i["name"])
                    if message.text in data and message.text != user["name"]:

                        for i in all_users:
                            if i["name"] == message.text:
                                location["usersData"][user["id"]]["playtennisConnection"] = i
                                break
                        bot.send_photo(user["id"], open("assets/basement/ping-pong.jpg", "rb"), caption="Ожидаем подтверждение от " + message.text + "...", reply_markup=exitmarkup)
                        n = user["name"]
                        location["usersData"][user["id"]]["stage"] = 3
                        bot.send_photo(location["usersData"][user["id"]]["playtennisConnection"]["id"], open("assets/basement/ping-pong.jpg", "rb"), caption=f"Игрок {n} предлагает вам сыграть в пинг-понг", reply_markup=choicemarkup)
                        location["usersData"][location["usersData"][user["id"]]["playtennisConnection"]["id"]]["playtennisConnection"] = user
                        location["usersData"][location["usersData"][user["id"]]["playtennisConnection"]["id"]]["stage"] = 2
                    else:
                        markupPlayers = types.ReplyKeyboardMarkup(resize_keyboard=True)
                        for i in all_users:
                            if i != user:
                                markupPlayers.add(i["name"])
                        markupPlayers.add("Отмена")
                        bot.send_message(user["id"], "Игрок не найден, возможно он уже вышел из подвала или играет с кем-то еще", reply_markup=markupPlayers)

            # base menu -----------------------------
            elif location["usersData"][user["id"]]["stage"] == 0:
                if message.text == "Магазин":
                    bot.send_photo(user["id"], open("assets/basement/shop.jpg", "rb"), caption="Вы зашли в магазин")
                elif message.text == "Пинг-понг":
                    if len(all_users) > 1:
                        location["usersData"][user["id"]]["playtennis"] = True
                        markupPlayers = types.ReplyKeyboardMarkup(resize_keyboard=True)
                        for i in all_users:
                            if i != user:
                                markupPlayers.add(i["name"])
                        markupPlayers.add("Отмена")
                        location["usersData"][user["id"]]["stage"] = 1
                        bot.send_photo(user["id"], open("assets/basement/ping-pong.jpg", "rb"), caption="Ты можеш сыграть, выбери игрока", reply_markup=markupPlayers)
                    else:
                        bot.send_message(user["id"], "В подвале никого нет, попробуй позже")
                elif message.text == "Выйти":
                    helpers.move_player(bot, user, "choice")
            
            time.sleep(1)
            location["usersData"][user["id"]]["wait"] = False
        else:
            bot.send_message(user["id"], "Не тыкай так часто :(")
    else:
        bot.send_message(user["id"], "Ждите окончания перехода...")

def events(bot, all_users, location=None):
    pass