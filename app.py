# coding: utf-8

import os

from flask import Flask, abort, request
from lineworks.talkbot_api import TalkBotApi


app = Flask(__name__)
talkbot = TalkBotApi(
    api_id=os.environ.get('API_ID'),
    private_key=os.environ.get('PRIVATE_KEY'),
    server_api_consumer_key=os.environ.get('SERVER_API_CONSUMER_KEY'),
    server_id=os.environ.get('SERVER_ID'),
    bot_no=os.environ.get('BOT_NO'),
    account_id=os.environ.get('ACCOUNT_ID'),
    room_id=os.environ.get('ROOM_ID'),
    domain_id=os.environ.get('DOMAIN_ID')
)


@app.route('/')
def index():
    return 'Start', 200


@app.route('/webhook', methods=['GET', 'HEAD', 'POST'])
def webhook():
    if request.method == 'GET':
        return 'Start', 200
    elif request.method == 'HEAD':
        return '', 200
    elif request.method == 'POST':
        action_type = request.json['action']['display']['translationKey']
        if action_type == 'action_comment_on_card':
            card_name = request.json['action']['data']['card']['name']
            user_name = request.json['action']['memberCreator']['fullName']
            comment = request.json['action']['data']['text']
            message = user_name + "さんがコメントしました。\n【カード】" + card_name + "\n【コメント】" + comment
            talkbot.send_text_message(send_text=message)
            return '', 200
        else:
            pass
    else:
        abort(400)


if __name__ == '__main__':
    app.run()