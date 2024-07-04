import asyncio
import time

a = True

def cycle():
    a = True
    time.sleep(1)
    a = False
    time.sleep(1)
    cycle()

def run():
    cycle()
    while True:
        print(a)

asyncio.run(run())