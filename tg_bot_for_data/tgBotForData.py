import requests
import telethon.tl.types
import telethon.tl.custom.file
from telethon import TelegramClient, events

from data import *
from datetime import datetime
import xlsxwriter
import MongoDB

## TZ мне

client = TelegramClient('client', API_ID, API_HASH).start(bot_token=API_TOKEN_TG_DATA)
database = MongoDB.Database()


@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    k = event.client.build_reply_markup([
        [telethon.tl.types.KeyboardButton(text='Скачать базу данных')]
    ])
    await event.respond("gtr", buttons=k)


@client.on(events.NewMessage(pattern='Скачать базу данных'))
async def send_data(event):

    workbook = xlsxwriter.Workbook('database.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.write(f'A{1}', "id")
    worksheet.write(f'B{1}', "from")
    worksheet.write(f'C{1}', "first_name")
    worksheet.write(f'D{1}', "phone_number")
    worksheet.write(f'E{1}', "date/time")

    col = 0
    row = 2
    for i in database.a:
        print(i)
        print(i.values())
        for data in enumerate(i.values()):
            for j in data:
                worksheet.write(row, col, str(j))
            col += 1
        row += 1
        col = 0

    await client.send_file(file='database.xlsx')

    workbook.close()


def main():
    client.run_until_disconnected()


if __name__ == '__main__':
    main()