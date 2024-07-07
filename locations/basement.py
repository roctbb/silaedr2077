import random
import time
from storage import users
import helpers

from telebot import types

basemarkup = helpers.create_keyboard([["Магазин", "Пинг-понг", "Выйти"]])

exitmarkup = helpers.create_keyboard([["Bыйти"]])

choicemarkup = helpers.create_keyboard([["Да", "Нет"]])

tennisgamemarkup = helpers.create_keyboard([["Слева", "Спереди", "Справа"]])

shopmarkup = helpers.create_keyboard([["Купить", "Продать"], ["Bыйти"]])

def enter(bot, user, all_users, location):
    if user["id"] not in location["usersData"]:
        bot.send_photo(user["id"], open("assets/basement/base.jpg", "rb"), caption=f"Вижу ты тут впервые, ну чтож, думаю сам разберешся)\nСейчас здесь тусуется {len(all_users)} игроков", reply_markup=basemarkup)
    else:
        bot.send_photo(user["id"], open("assets/basement/base.jpg", "rb"), caption=f"Снова привет братан)\nИгроков в подвале: {len(all_users)-1}", reply_markup=basemarkup)

    location["usersData"][user["id"]] = {
        "playtennisConnection": None, 
        "stage": 0, 
        "shieldChoice": [], 
        "attackChoice": 0, 
        "turn": -1, 
        "score": [0, 0],
        "wait": False, 
        "buyItem": [], 
        "sellItem": []
    }



def leave(bot, user, all_users, location=None):
    if location["usersData"][user["id"]]["playtennisConnection"] != None:
        bot.send_message(location["usersData"][user["id"]]["playtennisConnection"]["id"], "Твой противник резко вышел из подвала", reply_markup=basemarkup)
        location["usersData"][location["usersData"][user["id"]]["playtennisConnection"]["id"]]["stage"] = 0
        location["usersData"][location["usersData"][user["id"]]["playtennisConnection"]["id"]]["score"] = [0, 0]
        location["usersData"][location["usersData"][user["id"]]["playtennisConnection"]["id"]]["shieldChoice"] = []
        location["usersData"][location["usersData"][user["id"]]["playtennisConnection"]["id"]]["playtennisConnection"] = None
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
#-------------------------------------------------------------------------------------------
def message(bot, message, user, all_users, location=None):
    
    if user["location"] == "basement":
        if not location["usersData"][user["id"]]["wait"]:
            location["usersData"][user["id"]]["wait"] = True
            # shop sell cost
            if location["usersData"][user["id"]]["stage"] == 10:
                if message.text == "Bыйти":
                    location["usersData"][user["id"]]["stage"] = 8
                    bot.send_message(user["id"], "Ты вернулся назад", reply_markup=helpers.create_keyboard([["Назад"], user["inventory"]]))
                else:
                    if message.text.isdigit():
                        if user["id"] in list(location["StoreOffers"].keys()):
                            location["StoreOffers"][user["id"]].append([location["usersData"][user["id"]]["sellItem"], int(message.text)])
                            location["usersData"][user["id"]]["stage"] = 0
                            bot.send_message(user["id"], "Твой предмет добавлен в магазин", reply_markup=basemarkup)
                            users[user["id"]]["inventory"].remove(location["usersData"][user["id"]]["sellItem"])
                        else:
                            location["StoreOffers"][user["id"]] = [[location["usersData"][user["id"]]["sellItem"], int(message.text)]]
                            location["usersData"][user["id"]]["stage"] = 0
                            bot.send_message(user["id"], "Твой предмет добавлен в магазин", reply_markup=basemarkup)
                            users[user["id"]]["inventory"].remove(location["usersData"][user["id"]]["sellItem"])
                    else:
                        bot.send_message(user["id"], "Напиши целое положительно число")
            # shop buy confirmation
            elif location["usersData"][user["id"]]["stage"] == 9:
                if message.text == "Нет":
                    location["usersData"][user["id"]]["stage"] = 0
                    bot.send_message(user["id"], "Ты вышел из магазина", reply_markup=basemarkup)
                if message.text == "Да":
                    flag = True
                    for key in location["StoreOffers"].keys():
                        for i in location["StoreOffers"][key]:
                            if (i[0] + " " + str(i[1]) + "🍪") == (location["usersData"][user["id"]]["buyItem"][1] + " " + str(location["usersData"][user["id"]]["buyItem"][2]) + "🍪"):
                                flag = False
                    if not flag:
                        users[user["id"]]["inventory"].append(location["usersData"][user["id"]]["buyItem"][1])
                        users[user["id"]]["cookies"] -= location["usersData"][user["id"]]["buyItem"][2]
                        users[location["usersData"][user["id"]]["buyItem"][0]]["cookies"] += location["usersData"][user["id"]]["buyItem"][2]
                        text1 = location["usersData"][user["id"]]["buyItem"][1]
                        text2 = location["usersData"][user["id"]]["buyItem"][2]
                        bot.send_message(user["id"], f"Ты успешно купил {text1} за {text2}🍪", reply_markup=basemarkup)
                        location["usersData"][user["id"]]["stage"] = 0
                        bot.send_message(location["usersData"][user["id"]]["buyItem"][0], f"У тебя купили {text1} за {text2}🍪")
                        location["StoreOffers"][location["usersData"][user["id"]]["buyItem"][0]].remove([location["usersData"][user["id"]]["buyItem"][1], location["usersData"][user["id"]]["buyItem"][2]])
                    else:
                        bot.send_message(user["id"], "Предмет уже кто-то купил :(", reply_markup=basemarkup)
                        location["usersData"][user["id"]]["stage"] = 0
                    


            # shop sell choice
            elif location["usersData"][user["id"]]["stage"] == 8:
                if message.text == "Назад":
                    bot.send_message(user["id"], "Ты вернулся назад", reply_markup=shopmarkup)
                    location["usersData"][user["id"]]["stage"] = 6
                else:
                    if message.text in user["inventory"]:
                        flag = False
                        if user["inventory"]:
                            bot.send_message(user["id"], f"Введи сколько ты хочешь печенек🍪 за {message.text}", reply_markup=exitmarkup)
                            location["usersData"][user["id"]]["stage"] = 10
                            location["usersData"][user["id"]]["sellItem"] = message.text
            # shop buy choice
            elif location["usersData"][user["id"]]["stage"] == 7:
                if message.text == "Назад":
                    bot.send_message(user["id"], "Ты вернулся назад", reply_markup=shopmarkup)
                    location["usersData"][user["id"]]["stage"] = 6
                else:
                    flag = True
                    for key in location["StoreOffers"].keys():
                        for i in location["StoreOffers"][key]:
                            if message.text == i[0] + " " + str(i[1]) + "🍪":
                                flag = False
                                if user["cookies"] >= i[1]:
                                    text = str(i[1])
                                    text2 = i[0]
                                    print(i)
                                    location["usersData"][user["id"]]["buyItem"] = [key, i[0], i[1]]
                                    bot.send_message(user["id"], fr"Ты уверен что хочушь купить {text2} за {text}🍪?", reply_markup=choicemarkup)
                                    location["usersData"][user["id"]]["stage"] = 9
                                else:
                                    bot.send_message(user["id"], "У вас недостаточно печенек🍪 :(", reply_markup=basemarkup)
                                    location["usersData"][user["id"]]["stage"] = 0
                    if flag:
                        for key in location["StoreOffers"].keys():
                            for i in location["StoreOffers"][key]:
                                if message.text == "Снять с продажи " + i[0] and key == user["id"]:
                                    flag = False
                                    key1 = key
                                    ins = [i[0], i[1]]
                        
                        if flag:
                            bot.send_message(user["id"], "Такого предмета нет на рынке(возможно его уже кто-то купил)")
                        else:
                            if ins in location["StoreOffers"][key1]:
                                location["StoreOffers"][key1].remove(ins)
                                users[user["id"]]["inventory"].append(ins[0])
                                bot.send_message(user["id"], fr"Ты успешно снял предмет с продажи", reply_markup=shopmarkup)
                                location["usersData"][user["id"]]["stage"] = 6
                            else:
                                bot.send_message(user["id"], "Такого предмета нет на рынке(возможно его уже кто-то купил)")
            #shop base
            elif location["usersData"][user["id"]]["stage"] == 6:
                if message.text == "Bыйти":
                    bot.send_message(user["id"], "Ты вышел из магазина", reply_markup=basemarkup)
                    location["usersData"][user["id"]]["stage"] = 0
                elif message.text == "Купить":
                    if len(list(location["StoreOffers"].keys())) == 0:
                        n = []
                        buymarkup = helpers.create_keyboard(["Назад"])
                        bot.send_message(user["id"], "В магазине ничего не продается\nТы можешь выставить что-то первым!", reply_markup=buymarkup)
                        location["usersData"][user["id"]]["stage"] = 7
                    else:
                        n = []
                        for key in location["StoreOffers"].keys():
                            for i in location["StoreOffers"][key]:
                                if key != user["id"]:
                                    n.append(i[0] + " " + str(i[1]) + "🍪")
                                else:
                                    n.append("Снять с продажи " + i[0])
                        buymarkup = helpers.create_keyboard([["Назад"], n], rowsWidth=2)
                        bot.send_message(user["id"], "Выберите предложение", reply_markup=buymarkup)
                        location["usersData"][user["id"]]["stage"] = 7
                elif message.text == "Продать":
                    if len(user["inventory"]) == 0:
                        sellmarkup = helpers.create_keyboard(["Назад"])
                        bot.send_message(user["id"], "У тебя нет вещей :(", reply_markup=sellmarkup)
                        location["usersData"][user["id"]]["stage"] = 8               
                    else:
                        sellmarkup = helpers.create_keyboard([["Назад"], user["inventory"]])
                        bot.send_message(user["id"], "Выбери что выставить на продажу", reply_markup=sellmarkup)
                        location["usersData"][user["id"]]["stage"] = 8
            # pingpongMainGame
            # waiting 
            elif location["usersData"][user["id"]]["stage"] == 5:
                if message.text == "Bыйти":
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
                        if location["usersData"][location["usersData"][user["id"]]["playtennisConnection"]["id"]]["stage"] != 5:
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
                    
                    if location["usersData"][location["usersData"][user["id"]]["playtennisConnection"]["id"]]["stage"] != 5:
                            bot.send_photo(user["id"], open("assets/basement/ping-pong.jpg", "rb"), caption="Ты сделал выбор, ожидай противника...", reply_markup=exitmarkup)
                            location["usersData"][user["id"]]["stage"] = 5
                            location["usersData"][user["id"]]["turn"] *= -1
                    else:
                        checkAttacker(bot, message, user, all_users, location)
                        location["usersData"][user["id"]]["turn"] *= -1


            # cansel if u are tennis host + waiting for opponent to confirm -----------------------------
            elif location["usersData"][user["id"]]["stage"] == 3:
                if message.text == "Bыйти":
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
                    bot.send_photo(user["id"], open("assets/basement/shop.jpg", "rb"), caption="Вы зашли в магазин", reply_markup=shopmarkup)
                    location["usersData"][user["id"]]["stage"] = 6
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
    #for i in all_users:
    #    bot.send_message(i["id"], "Ивент!!")

def reset(user, location):
    if user["id"] in location["StoreOffers"]:
        for i in location["StoreOffers"][user["id"]]:
            location["StoreOffers"]["-1"].append(i)
        location["StoreOffers"][user["id"]] = []