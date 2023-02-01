import telethon.tl.types
from telethon import TelegramClient, events
from data import *
import MongoDB

bot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=API_TOKEN_TG)

database = MongoDB.Database()


@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    k = event.client.build_reply_markup([
        [telethon.tl.types.KeyboardButtonRequestPhone(text='Для дальнейшей работы с ботом, необходимо '
                                                           'поделиться номером телефона')]
    ])
    await event.respond("Здравствуйте", buttons=k)


@bot.on(events.NewMessage())
async def contact(message):
    if message.media is not None:
        # Вывод в txt файл
        # file = open('abc.txt', 'a')
        # file.write(str(message.media.phone_number + "\n"))
        # file.close()
        name = message.media.first_name
        phone = message.media.phone_number
        #print(name, phone)
        database.posts.insert_one({"first_name": name, "phone_number": phone})  # Запись в БД
        #print(message.media)


def main():
    bot.run_until_disconnected()


if __name__ == '__main__':
    main()