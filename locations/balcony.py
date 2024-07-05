from helpers import get_all_users


def enter(bot, user, all_users, location, previous_location=None):
    bot.send_message(user["id"], "Вы вышли на балкон")


def leave(bot, user, all_users, location=None):
    pass


def message(bot, message, user, all_users, location=None):
    if message.text.startswith("/shout"):
        if len(message.text.split()) > 1:
            shout(bot, " ".join(message.text.split()[1:]))
        else:
            bot.send_message(
                user["id"], "Чтобы крикнуть напишите /shout {фраза которую хотите сказать}")


def events(bot, all_users):
    pass


def shout(bot, message):
    for user in get_all_users():
        if user["location"] != "basement":
            bot.send_message(user["id"], message)
