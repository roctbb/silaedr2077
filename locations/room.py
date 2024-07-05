from helpers import *


basemarkup = create_keyboard([["Выйти на балкон"]])

def enter(bot, user, all_users, location):
    if not location["usersData"].get(user["id"]):
        bot.send_photo(user["id"], open("assets/room/scary_dark_room.jpg", "rb"),
                caption = "Ты зашел в комнату, но ты незнаешь в какую. В комнате темно и издалека доносится голос Инги Александровны. В конце концов ты выбежал от туда и решил выбрать комнату нормально")
        move_player(bot, user, "choice")
        return
    number = location["usersData"][user["id"]]["room"]
    bot.send_message(user["id"], f"Ты зашел в комнату {number}", reply_markup=basemarkup)

def leave(bot, user, all_users, location):
    pass

def message(bot, message, user, all_users, location):
    if message.text == "Выйти на балкон":
        move_player(bot, user, "balcony")
        return




def events(bot, all_users, location):
    pass