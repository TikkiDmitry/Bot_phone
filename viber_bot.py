from flask import Flask, request, Response
from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages.text_message import TextMessage
from data import API_TOKEN_VIBER
from viberbot.api.viber_requests import ViberMessageRequest
import MongoDB

app = Flask(__name__)
viber = Api(BotConfiguration(
    name='Bob',
    avatar='',
    auth_token=API_TOKEN_VIBER
))

database = MongoDB.Database()


@app.route('/', methods=['POST'])
def incoming():

    # Каждое сообщение viber подписано, можно проверить подпись, используя этот метод
    if not viber.verify_signature(request.get_data(), request.headers.get('X-Viber-Content-Signature')):
        return Response(status=403)

    # Способ получения объекта запроса
    viber_request = viber.parse_request(request.get_data())

    if isinstance(viber_request, ViberMessageRequest):
        keyboard = {                                           # Настройка клавиатуры бота
            "DefaultHeight": True,
            "BgColor": "#FFFFFF",
            "Type": "keyboard",
            "Buttons": [
                {
                    "BgColor": "#e6f5ff",
                    "BgLoop": True,
                    "ActionType": "share-phone",
                    "ActionBody": "reply",
                    "Text": "Для дальнейшей работы с ботом необходим номер телефона"
                }
            ]
        }
        message = viber_request.message

        viber.send_messages(viber_request.sender.id, [          # Показ кнопки пользователю для отправки номера
            TextMessage(text=' ', keyboard=keyboard,
                        min_api_version=3)
        ])
        name = message.contact.name
        phone = message.contact.phone_number
        database.posts.insert_one({"first_name": name, "phone_number": phone})  # Запись в БД
        # print(message.contact)
        # print(name, phone)

    return Response(status=200)


if __name__ == "__main__":
    context = ('server.crt', 'server.key')
    app.run(port="8000")