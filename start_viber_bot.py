import subprocess
import os

from time import sleep

if __name__=="__main__":
    # subprocess.call(["python", "./bots/viber/client.py"], env=os.environ.copy(), executable=r"s:/Проекты/Bot_phone/env/Scripts/python.exe")
    subprocess.Popen(["python", "./bots/telegram/auth.py"], env=os.environ.copy(), executable=r"s:/Проекты/Bot_phone/env/Scripts/python.exe")
    sleep(3)
    subprocess.Popen(["python", "./bots/whatsapp/whatsapp_bot.py"], env=os.environ.copy(), executable=r"s:/Проекты/Bot_phone/env/Scripts/python.exe")
    