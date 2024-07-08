import telebot
from storage import *
from helpers import *

bot = get_bot()

basemarkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
it1 = types.KeyboardButton("Да")
it2 = types.KeyboardButton("Нет")
basemarkup.add(it1, it2)


def test_name(message):
    if message.text == "Да":
        name = ""
        if message.from_user.first_name != None:
            name += message.from_user.first_name
        else:
            name += "Anonim"
        if message.from_user.last_name != None:
            name += " "
            name += message.from_user.last_name
        user = users[str(message.from_user.id)]
        user['inventory'][user['inventory'].index(
            'badge - ' + name)] = 'badge - ' + user['name']
        bot.send_message(user["id"], f"Ваше имя: {user['name']}.")
        move_player(bot, users[str(message.from_user.id)], "choice")
    else:
        msg = bot.send_message(user["id"], f"Введите имя.")
        bot.register_next_step_handler(msg, set_name)


def set_name(message):
    user = users[str(message.from_user.id)]
    names = [users[i]['name']for i in users.keys()]
    if message.text not in names:
        user['name'] = message.text
        msg2 = bot.send_message(
            user["id"], f"Ваше имя: {user['name']}.", reply_markup=basemarkup)
        bot.register_next_step_handler(msg2, test_name)
    else:
        msg = bot.send_message(user["id"], "Имя занято.\nВведите имя.")
        bot.register_next_step_handler(msg, set_name)


@bot.message_handler(content_types=['text'])
def process_message(message):
    print(message.from_user.first_name + " >> " + message.text)
    if not is_registered(message):
        add_user(message)
        user = users[str(message.from_user.id)]
        msg = bot.send_message(user["id"], f"Введите имя.")
        bot.register_next_step_handler(msg, set_name)
    else:
        user = users[str(message.from_user.id)]
        if message.text == "/locations":
            bot.send_message(user["id"], "/" +
                                '\n/'.join(locations.keys()))
        elif message.text == "/stats":
            give_stats(user, bot)
        elif message.text.startswith("/name"):
            user['inventory'][user['inventory'].index(
                f'Бейджик - {user["name"]}')] = 'Бейджик - ' + message.text[6:]
            user['name'] = message.text[6:]
            bot.send_message(user["id"], "Вы сменили имя." +
                                "\n" + "Ваше имя : " + user['name'] + ".")
        elif message.text.startswith("/") and message.text.strip('/') in locations:
            move_player(bot, user, message.text.strip('/'))
        else:
            module = get_module(user)
            all_users = get_neighbours(user)

            module.message(bot, message, user, all_users,
                            locations[user['location']])

            if user["corners"] == 0 or user["health"] == 0:
                restart(message)

    save_data()


bot.polling(none_stop=True)
