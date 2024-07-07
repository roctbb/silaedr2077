import telebot
from storage import *
from helpers import *

bot = get_bot()


@bot.message_handler(content_types=['text'])
def process_message(message):
    print(message.from_user.first_name + " >> " + message.text)
    if not is_registered(message):
        add_user(message)
        move_player(bot, users[str(message.from_user.id)], "choice")
    else:
        user = users[str(message.from_user.id)]
        if user["corners"] == 0:
            restart(message)
        else:
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

    save_data()


bot.polling(none_stop=True)
