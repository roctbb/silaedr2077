import telebot
from storage import *
from helpers import *

bot = get_bot()


def set_name(message):
    user = users[str(message.from_user.id)]
    names = [users[i]['name']for i in users.keys()]
    if message.text not in names:
        user['inventory'][user['inventory'].index(
            f'Бейджик - ' + user['name'])] = 'Бейджик - ' + message.text
        user['name'] = message.text
        bot.send_message(user["id"], f"Ваше имя: {user['name']}.")
        bot.send_message(user["id"], "Выберитя куда пойти.")
        move_player(bot, user, 'choice')
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
        if user["corners"] == 0:
            restart(message)
        else:
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

    save_data()


bot.polling(none_stop=True)
