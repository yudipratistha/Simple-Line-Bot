# mybot/app.py

import os
import json
from decouple import config
from flask import (
    Flask, request, abort
)
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import InvalidSignatureError
from linebot.models import Postback, MessageTemplateAction, MessageEvent, ButtonsTemplate, TemplateSendMessage, \
    TextMessage, URIImagemapAction, PostbackEvent, PostbackTemplateAction, SendMessage, TextSendMessage
# from flaskext.mysql import MySQL
import pymysql

# mysql = MySQL()
app = Flask(__name__)

# Connect to the database



# get LINE_CHANNEL_ACCESS_TOKEN from your environment variable
line_bot_api = LineBotApi(
    config("LINE_CHANNEL_ACCESS_TOKEN",
           default=os.environ.get('LINE_ACCESS_TOKEN'))
)
# get LINE_CHANNEL_SECRET from your environment variable
handler = WebhookHandler(
    config("LINE_CHANNEL_SECRET",
           default=os.environ.get('LINE_CHANNEL_SECRET'))
)

@app.route("/callback", methods=['POST'])
def callback():
    conn = pymysql.connect('180.252.74.52', 'yudi', '123123', 'db_bot')
    cur = conn.cursor()

    signature = request.headers['X-Line-Signature']


    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)


    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    print("body "+ body)
    body = json.loads(body)
    msg = body['events'][0]['message']
    idcht = msg['id']
    txt = msg['text']
    usrid = body['events'][0]['source']['userId']
    try:
        groupid = body['events'][0]['source']['groupId']
    except:
        groupid = None
    # print("aaaaa" +groupid)
    # cur.execute("INSERT INTO tb_inbox (usr_id, cht_id, messages) VALUES ('%s', %s, '%s')" % (usrid, idcht, txt))
    # conn.commit()
    # cur.close()
    if(groupid is not None):
        print("if")
        try:
            cur.execute("INSERT INTO inbox (usr_id, group_id, cht_id, messages) VALUES ('%s', '%s', '%s', '%s')" % (usrid, groupid, idcht, txt))
            conn.commit()
            print(txt)
        except Exception as e:
            print(e)
    else:
        try:
            cur.execute("INSERT INTO inbox (usr_id, cht_id, messages) VALUES ('%s', '%s', '%s')" % (
                usrid, idcht, txt))
            conn.commit()
            print(txt)
        except Exception as e:
            print(e)
    conn.close()
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    if event.message.text == "aaaa":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text)
        )
    text = event.message.text
    # if text == 'buttons':
    #     buttons_template = ButtonsTemplate(
    #         title='My buttons sample', text='Hello, my buttons', actions=[
    #             URIImagemapAction(label='Go to line.me', uri='https://line.me'),
    #             PostbackTemplateAction(label='ping', data='ping'),
    #             PostbackTemplateAction(label='ping with text', data='ping', text='ping'),
    #             MessageTemplateAction(label='Translate Rice', text='米')
    #         ])
    #     template_message = TemplateSendMessage(
    #         alt_text='Buttons alt text', template=buttons_template)
    #     line_bot_api.reply_message(event.reply_token, template_message)
    # # print(event.message.text)
    # if event.message.text == "aaaa":
    #     line_bot_api.reply_message(
    #         buttons_template_message
    #     )

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)