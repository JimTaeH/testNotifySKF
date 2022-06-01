import json
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('YuiRCG1kEfW7kLxKszY+wDfcnvOjA8tVKDp1UjK/vW+qic1MXFLTiWecx4BE2c9w9lOqLvXD9C4rIvi7kWQzdRlOJEcrydOnnqpwi/aNJvNUVBmif4tSr0dzAlaLuACOmK8lLJmOWWaEK6WCeCdfUgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('b8699fd043b6bae3df9cd241492cc596')


@app.route('/')
def index():
    return "Hello World! From Flask"


@app.route('/webhook', methods=['POST'])
def callback():
    json_line = request.get_json(force=False,cache=False)
    json_line = json.dumps(json_line)
    decoded = json.loads(json_line)
    no_event = len(decoded['events'])
    for i in range(no_event):
        event = decoded['events'][i]
        event_handle(event)
    return '',200

def event_handle(event):
    print(event)
    try:
        userId = event['source']['userId']
    except:
        print('error cannot get userId')
        return ''

    try:
        rtoken = event['replyToken']
    except:
        print('error cannot get rtoken')
        return ''

    try:
        eventType = event['type']
    except:
        print('Cannot get Event Type')
        return ''

    try:
        timestamp = event['timestamp']
    except:
        print('Cannot get TimeStamp')
        return ''
    try:
      if eventType == 'message':
          msgId = event['message']['id']
          msgType = event['message']['type']
          msg = event['message']['text']
          msgnum = event['message']['text'].replace('.','')
      elif eventType == 'postback':
          pbData = event["postback"]["data"]
    except:
        print('Cannot get Data from webhook')

    if eventType == 'message':
        replyObj = TextSendMessage(text=msg)
        line_bot_api.reply_message(rtoken, replyObj)

if __name__ == "__main__":
    app.run(debug=True)