import random
import helpers
buttons = [['продажа', 'топиться'],['вылезти', 'ловить']]
but = helpers.create_keyboard(buttons, rowsWidth=2)
def enter(bot, user, all_users, location):

    bot.send_photo(user["id"], open("assets/swamp/Swamp.png", "rb"), caption = "Вы вошли на болото. Здесь вы можете обменять Ирине Николаевне пойманых вами организмов с помощью 'продажа', а так же ловить эти организмы, утопившись в болоте с помощью 'топиться' ", reply_markup=but)

def leave(bot, user, all_users, location):
    pass

catches = [ {   "name": "stonefly",
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
            },{
                "name": "snail",
                "runame": "прудовик",
                "propobilyty": 70,
                "cost": 3,
                "rep": 2,
                "fun": 1
            }]
def message(bot, message, user, all_users, location):
    if message.text == "топиться":
        user["action"] = "drowning"
        bot.send_message(user["id"], "Вы начали топиться в болоте. Можете прописать 'ловить', чтобы поймать кого-то, или 'вылезти', чтобы перестать топиться", reply_markup=but)
    elif message.text == "ловить":
        if user["action"] == "drowning":
            bot.send_message(user["id"], "Вы начинаете ловить кого то в болоте.", reply_markup=but)
            catch=random.choice(catches)
            if catch["propobilyty"] >= random.randint(0,100):
                st="Вы поймали нечто! И это - "+catch["runame"]+". Ecли вы хотите вылезти из болота, пропишите 'вылезти'"
                bot.send_message(user["id"], st, reply_markup=but)
                user["inventory"].append(catch["name"])
            else:
                bot.send_message(user["id"], "Вам не удалось ничего поймать. Можете попробовать снова, или вылезти из болота 'вылезти'", reply_markup=but)
    elif message.text == "продажа":
        if user["action"] != "drowning":
            
            length_of_sell=0
            while ("leech" in user["inventory"] or "snail" in user["inventory"] or "stonefly" in user["inventory"] or "frog" in user["inventory"]) and length_of_sell<1000:
                counter_of_swamp_sell = -1
                length_of_sell+=1
                for i in user["inventory"]:
                    counter_of_swamp_sell += 1
                    for j in catches:
                        if i==j["name"]:
                            user["fun"]+=j["fun"]
                            user["cookies"]+=j["cost"]
                            user["reputation"]+=j["rep"]
                            if counter_of_swamp_sell<len(user["inventory"]):
                                del user["inventory"][counter_of_swamp_sell]
                            counter_of_swamp_sell-=1 

                        
            bot.send_message(user["id"], "Вы обменяли найденных обитателей болота Ирине Николаевне на печеньки и репутацию, и получили удовольствие", reply_markup=but)
            if user["fun"]>100:
                user["fun"]=100
            if user["reputation"]>100:
                user["reputation"]=100
        else:
            bot.send_message(user["id"], "Вы все еще тоните!", reply_markup=but)
    elif message.text == "вылезти":
        if user["action"] == "drowning":
            user["action"] = "stay"
            bot.send_message(user["id"], "Вы перестали тонуть в болоте", reply_markup=but)
        else:
            bot.send_message(user["id"], "Вы еще не тонете", reply_markup=but)
    else:
        bot.send_message(user["id"], "Вы на болоте", reply_markup=but)

def events(bot, all_users, location):
    pass