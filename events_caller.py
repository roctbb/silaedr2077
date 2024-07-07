from storage import *
from helpers import *
import time
from threading import Thread

bot = get_bot()


def start():
    import silaedr2077


t = Thread(target=start, args=())
t.daemon = True
t.start()

while True:
    for location in locations.keys():
        all_users = list(
            filter(lambda x: x["location"] == location, users.values()))
        # print(all_users, '                 ', locations[location])
        if len(all_users) > 0:
            print(1)
            module = get_module(all_users[0])
            module.events(bot, all_users, locations[location])

    time.sleep(30)
