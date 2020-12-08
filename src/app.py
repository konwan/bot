import os
import datetime

# for atom use
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"..")))

from lib.robot.time import *
from lib.robot.movie import *
from lib.util.outputdata import OutputData
from lib.variables import *
from lib.util.messages import *

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    StickerMessage, StickerSendMessage,
    TemplateSendMessage, ButtonsTemplate,
    URITemplateAction, MessageTemplateAction,
    ConfirmTemplate, CarouselTemplate, CarouselColumn, PostbackTemplateAction,
    PostbackEvent,LocationMessage, LocationSendMessage
)

# add access token
app = Flask(__name__)
LINE_CHANNEL_ACCESS_TOKEN = os.environ['LINE_CHANNEL_ACCESS_TOKEN_HL']
LINE_CHANNEL_SECRET = os.environ['LINE_CHANNEL_SECRET_HL']
opd = OutputData()
# line bot
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
# event handler
handler = WebhookHandler(LINE_CHANNEL_SECRET)
UserID= 'Ub4006477cb3f1f8765657b972b7c9e2b'

@app.route("/hi", methods=['GET'])
def hi():
    return "hi"

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        # handle webhook body
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    # for event in events:
    #     if not isinstance(event, MessageEvent):
    #         continue
    #     if not isinstance(event.message, TextMessage):
    #         continue
    #
    #     line_bot_api.reply_message(
    #         event.reply_token,
    #         TextSendMessage(text=event.message.text)
    #     )
    # line_bot_api.push_message(UserID, TextSendMessage(text='Hello World!'))
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_text(event):
    text = event.message.text
    user_id = event.source.user_id
    msg = "{} send {} with {}".format(user_id, event.message.id, event.message.text)
    sendmessage = TextSendMessage(text=greeting())

    if text == "basic":
        profile = line_bot_api.get_profile(user_id)
        basicinfo = "{} {} {}".format(profile.display_name, profile.picture_url, profile.status_message)
        sendmessage = TextSendMessage(text=basicinfo)

    if text == "button":
         sendmessage = TemplateSendMessage(
            alt_text = not_support(),
            template = ButtonsTemplate(
                title = 'choose service',
                text = 'which one?',
                thumbnail_image_url = 'https://i.imgur.com/kzi5kKy.jpg',
                actions = [
                    PostbackTemplateAction(
                        label = "高鐵時刻表查詢",
                        text = "time",
                        data = "time"
                    ),
                    URITemplateAction(
                        label = 'intro',
                        uri = 'https://youtu.be/1IxtWgWxtlE'
                    ),
                    PostbackTemplateAction(
                        label = "eyny movie",
                        text = "movie movie",
                        data = "eyny"
                    )
                ]
            )
            )
    if text == "confirm":
        sendmessage = TemplateSendMessage(
            alt_text = not_support(),
            template = ConfirmTemplate(
              text = 'Give me a answer!!!',
              actions=[
                 MessageTemplateAction(label='Yes', text='Yes!'),
                 MessageTemplateAction(label='No', text='No!')
              ])
        )
    if text == "carousel":
        sendmessage = TemplateSendMessage(
            alt_text = not_support(),
            template = CarouselTemplate(
                columns=[
                CarouselColumn(text='hoge1', title='fuga1', actions=[
                    URITemplateAction(
                        label='Go to line.me', uri='https://line.me'),
                    PostbackTemplateAction(label='ping', text='idiot', data='congrat')
                ]),
                CarouselColumn(text='hoge2', title='fuga2', actions=[
                    PostbackTemplateAction(
                        label='congrat', text='postback text',
                        data='action=buy&itemid=1'),
                    MessageTemplateAction(label='Translate Rice', text='米')
                ])]
        ))

    line_bot_api.reply_message(event.reply_token, sendmessage)
    update = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = [[update, event.source.user_id, event.message.id, event.message.text]]
    opd.outputData(DATADIR, 'linelog', data)

# sticker massage
@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker(event):
    package_id = event.message.package_id
    sticker_id = event.message.sticker_id
    msg = "{} {}".format(package_id, sticker_id)
    if package_id not in ['1','2','3'] :
        sticker_ids = sticker(mood="normal", cat=1)
        sticker_message = StickerSendMessage(package_id=sticker_ids[0], sticker_id=sticker_ids[1])
    else :
        sticker_message = StickerSendMessage(package_id=package_id, sticker_id=sticker_id)

    line_bot_api.reply_message(event.reply_token, [sticker_message,TextSendMessage(text=msg)])

@handler.add(MessageEvent, message=LocationMessage)
def handle_location(event):
    msg = "latitude: {}  longitude: {}".format(event.message.latitude, event.message.longitude)
    line_bot_api.reply_message(
        event.reply_token,
        [LocationSendMessage(
            title=event.message.title, address=event.message.address,
            latitude=event.message.latitude, longitude=event.message.longitude),
         TextSendMessage(text=msg)]
    )

@handler.add(PostbackEvent)
def handle_postback(event):
    # {"postback": {"data": "action=buy&itemid=1"},
    # "replyToken": "7694f4927b2749e3917cd5a25c7d98bc",
    # "source": {"type": "user", "userId": "Ub4006477cb3f1f8765657b972b7c9e2b"},
    # "timestamp": 1490005606175, "type": "postback"}

    if event.postback.data == "eyny":
        msg = eynyMovie()
    if event.postback.data == "time":
        thr = THR()
        thr.crawl_data()
        msg = thr.answer

    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=msg))

if __name__ == "__main__":
    app.run()
    # from lib.robot.bot import EMBot
    # a= EMBot()
    # a.trace()
