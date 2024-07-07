import telebot
from storage import *
from helpers import *

bot = get_bot()


@bot.message_handler(content_types=['text'])
def process_message(message):
    print(message.from_user.first_name + " >> " + message.text)
    if not is_registered(message):
        add_user(message)

    user = users[str(message.from_user.id)]

    if message.text == "/locations":
        bot.send_message(user["id"], "/" + '\n/'.join(locations.keys()))
    elif message.text == "/start":
        bot.send_message(user["id"], f"Привет " + user['name'] + "." +
                         "\n" + "Если это имя тебя не устраевает пропиши /name <имя>.")
        move_player(bot, user, 'choice')
    elif message.text == "/stats":
        give_stats(user, bot)
    elif message.text.startswith("/") and message.text.strip('/') in locations:
        move_player(bot, user, message.text.strip('/'))
    elif message.text.startswith("/name"):
        user['inventory'][user['inventory'].index(
            f'badge - {user["name"]}')] = 'badge - ' + message.text[6:]
        user['name'] = message.text[6:]
        bot.send_message(user["id"], "Вы сменили имя." +
                         "\n" + "Ваше имя : " + user['name'] + ".")
        print(user['name'])
    else:
        module = get_module(user)
        all_users = get_neighbours(user)

        module.message(bot, message, user, all_users,
                       locations[user['location']])

    save_data()


bot.polling(none_stop=True)
