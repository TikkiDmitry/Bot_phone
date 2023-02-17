from dotenv import load_dotenv
load_dotenv("../../.env")

import os
import argparse
from datetime import datetime

from flask import Flask, request, Response

from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages.text_message import TextMessage
from viberbot.api.viber_requests import ViberMessageRequest

# import database
API_TOKEN_VIBER = os.getenv("API_TOKEN_VIBER")

app = Flask(__name__)
viber = Api(BotConfiguration(
    name='Bob',
    avatar='',
    auth_token=API_TOKEN_VIBER
))
# database = database.Database()


@app.route('/', methods=['POST'])
def incoming():
    if not viber.verify_signature(request.get_data(), request.headers.get('X-Viber-Content-Signature')):
        return Response(status=403)

    viber_request = viber.parse_request(request.get_data())
    if isinstance(viber_request, ViberMessageRequest):
        keyboard = {
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

        viber.send_messages(viber_request.sender.id, [
            TextMessage(text=' ', keyboard=keyboard,
                        min_api_version=3)
        ])
        name = message.contact.name
        phone = message.contact.phone_number
        # database.posts.insert_one({"from": "Viber", "first_name": name, "phone_number": phone, "date/time": str(datetime.now())})

    return Response(status=200)


if __name__ == "__main__":
    # curl -# -i -g -H "X-Viber-Auth-Token:ТОКЕН" -d @viber.json -X POST
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1", type=str)
    parser.add_argument("--port", default=8000, type=int)
    args = parser.parse_args()
    app.run(host=args.host, port=args.port)