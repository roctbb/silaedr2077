import telebot
from storage import *
from helpers import *

bot = get_bot()


@bot.message_handler(content_types=['text'])
def process_message(message):
    if not is_registered(message):
        add_user(message)

    user = users[message.from_user.id]

    if message.text == "/locations":
        bot.send_message(user["id"], "/" + '\n/'.join(locations.keys()))
    elif message.text == "/stats":
        give_stats(user, bot)
    elif message.text.startswith("/") and message.text.strip('/') in locations:
        move_player(bot, user, message.text.strip('/'))
    else:
        module = get_module(user)
        all_users = get_neighbours(user)

        module.message(bot, message, user, all_users,
                       locations[user['location']])


bot.polling(none_stop=True)
