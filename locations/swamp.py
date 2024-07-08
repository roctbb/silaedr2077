import random
import helpers
import time
buttons = [['продать', 'Топиться'], ['вылезти', 'Ловить', 'Выйти']]
but = helpers.create_keyboard(buttons, rowsWidth=2)


def enter(bot, user, all_users, location):
    realtime = time.localtime()
    current_time = time.strftime("%YYYY:%MM:%DD", realtime)
    if user["id"] not in list(location["usersData"].keys()):
        location["usersData"][user["id"]] = {
            "wait": False,
            "enters": 1,
            "catching": 0,
            "lastEnter": current_time
        }
    else:
        if current_time != location["usersData"][user["id"]]["lastEnter"]:
            location["usersData"][user["id"]]["enters"] = 0
        location["usersData"][user["id"]]["enters"] += 1
        location["usersData"][user["id"]]["lastEnter"] = current_time

    bot.send_photo(user["id"], open("assets/swamp/Swamp.png", "rb"),
                   caption="Вы вошли на болото. Здесь вы можете обменять Ирине Николаевне пойманых вами организмов с помощью 'продажа', а так же ловить эти организмы, утопившись в болоте с помощью 'топиться' ", reply_markup=but)


def leave(bot, user, all_users, location):
    pass


catches = [{"name": "Веснянка",
            "runame": "веснянка",
            "propobilyty": 70,
            "cost": 14,
            "rep": 8,
            "fun": 5
            }, {
    "name": "Лягушка",
                "runame": "лягушка",
                "propobilyty": 50,
                "cost": 10,
                "rep": 3,
                "fun": 7
}, {
    "name": "Пиявка",
                "runame": "пиявка",
                "propobilyty": 40,
                "cost": 12,
                "rep": 4,
                "fun": 1
}, {
    "name": "Улитка",
                "runame": "улитка",
                "propobilyty": 70,
                "cost": 6,
                "rep": 2,
                "fun": 1
}, {
    "name": "КЛАД",
                "runame": "КЛАД",
                "propobilyty": 2,
                "cost": 500,
                "rep": 10,
                "fun": 1
}]


def message(bot, message, user, all_users, location):
    if message.text == "Топиться":
        user["action"] = "drowning"
        bot.send_message(
            user["id"], "Вы начали топиться в болоте. Можете прописать 'ловить', чтобы поймать кого-то, или 'вылезти', чтобы перестать топиться", reply_markup=but)
    elif message.text == "Ловить":
        if user["action"] == "drowning":
            if not location["usersData"][user["id"]]["wait"]:
                if location["usersData"][user["id"]]["cathcing"] >= 10:
                    location["usersData"][user["id"]]["wait"] = True
                    bot.send_message(
                        user["id"], "Вы начинаете ловить кого то в болоте.", reply_markup=but)
                    catch = random.choice(catches)
                    location["usersData"][user["id"]]["catching"] += 1
                    if catch["propobilyty"] >= random.randint(0, 100):
                        st = "Вы поймали нечто! И это - " + \
                            catch["runame"] + \
                            ". Ecли вы хотите вылезти из болота, пропишите 'вылезти'"

                        bot.send_message(user["id"], st, reply_markup=but)
                        user["inventory"].append(catch["name"])
                    else:
                        bot.send_message(
                            user["id"], "Вам не удалось ничего поймать. Можете попробовать снова, или вылезти из болота 'вылезти'", reply_markup=but)
                    time.sleep(10)
                    location["usersData"][user["id"]]["wait"] = False
                else:
                    bot.send_message(
                        user["id"], "Нельзя ловить на болоте больше 10 раз за день! Вы так замерзните!", reply_markup=but)
            else:
                if random.randint(0, 5) == 0:
                    bot.send_message(
                        user["id"], "Ловить живность можно раз в 10 секунд", reply_markup=but)
        else:
            bot.send_message(
                user["id"], "Сначала нужно утопиться", reply_markup=but)
    elif message.text == "продаnm":
        if user["action"] != "drowning":

            length_of_sell = 0
            while ("КЛАД" in user["inventory"] or "Пиявка" in user["inventory"] or "Улитка" in user["inventory"] or "Веснянка" in user["inventory"] or "Лягушка" in user["inventory"]) and length_of_sell < 1000:
                counter_of_swamp_sell = -1
                length_of_sell += 1
                for i in user["inventory"]:
                    counter_of_swamp_sell += 1
                    for j in catches:
                        if i == j["name"]:
                            user["fun"] += j["fun"]
                            user["cookies"] += j["cost"]
                            user["reputation"] += j["rep"]
                            if counter_of_swamp_sell < len(user["inventory"]):
                                del user["inventory"][counter_of_swamp_sell]
                            counter_of_swamp_sell -= 1

            bot.send_message(
                user["id"], "Вы обменяли найденных обитателей болота Ирине Николаевне на печеньки и репутацию, и получили удовольствие", reply_markup=but)
            if user["fun"] > 100:
                user["fun"] = 100
            if user["reputation"] > 100:
                user["reputation"] = 100
        else:
            bot.send_message(
                user["id"], "Вы все еще тоните!", reply_markup=but)
    elif message.text == "вылезти":
        if user["action"] == "drowning":
            user["action"] = "stay"
            bot.send_message(
                user["id"], "Вы перестали тонуть в болоте", reply_markup=but)
        else:
            bot.send_message(user["id"], "Вы еще не тонете", reply_markup=but)
    elif message.text == 'Выйти':
        helpers.move_player(bot, user, "choice")
    else:
        bot.send_message(user["id"], "Вы на болоте", reply_markup=but)


def events(bot, all_users, location):
    pass


def reset(user, location):
    pass
