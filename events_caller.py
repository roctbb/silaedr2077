from modules import *
from helpers import *
import time
from threading import Thread

bot = get_bot()

def start():
    while True:
        try:
            import silaedr2077
        except Exception as e: print(e)

t = Thread(target=start, args=( ))
t.daemon = True
t.start()

while True:
    for key in available_modules.keys():
        module = available_modules[key]
        all_users = list(filter(lambda x: x["location"] == key, users.values()))
        module.events(bot, all_users, locations[key])
        
    time.sleep(300)