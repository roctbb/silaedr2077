def enter(bot, user, all_users, location):
    bot.send_message(user["id"], "Вы вошли на болото")

def leave(bot, user, all_users, location):
    pass

catches = [ {   "name": "caddis fly",
                "runame": "веснянка",
                "propobilyty": 20,
                "cost": 7,
                "rep": 8,
                "fun": 5
            },{
                "name": "frog",
                "runame": "лягушка",
                "propobilyty": 30,
                "cost": 5,
                "rep": 3,
                "fun": 7
            },{
                "name": "leech",
                "runame": "пиявка",
                "propobilyty": 10,
                "cost": 6,
                "rep": 4,
                "fun": 1
            }]
def message(bot, message, user, all_users, location):
    if message.text == "/drown":
        user["action"] = "drowning"
        bot.send_message(user["id"], "Вы начали топиться в болоте.")
    elif message.text == "/catch":
        if user["action"] == "drowning":
            bot.send_message(user["id"], "Вы начинаете ловить кого то в болоте.")
            catch=random.choice(catches)
            if catch["propobilyty"] >= random.randint(0,100):
                st="Вы поймали нечто! И это - "+catch["runame"]
                bot.send_message(user["id"], st)
                user["inventory"].append(catch["name"])
            else:
                bot.send_message(user["id"], )
    elif message.text == "/sell":
        if user["action"] != "drowning":
            for i in user["inventory"]:
                for j in catches:
                    if i==j[""]:
                        pass




    bot.send_message(user["id"], "Вы на болоте")

def events(bot, all_users, location):
    pass