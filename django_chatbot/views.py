from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage
import os

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)  # 傳入的事件
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            print("event", event.message.id)
            # print("event", type(event))
            if isinstance(event, MessageEvent):  # 如果有訊息事件
                print("message", event.message)
                message = []

                if event.message.type == 'text':
                    mtext = event.message.text
                    if "嗨" in mtext:
                        text_ = "哈囉你好"
                    else:
                        text_ = 'What?'

                    print("type of mtext: {}".format(type(mtext)))
                    message.append(TextSendMessage(text=text_))

                # elif event.message.type == 'sticker':
                #     text_ = event.message.id
                #     message.append(TextSendMessage(text=text_))
                #
                # elif event.message.type == 'image':
                #     text_ = event.message.id
                #     message.append(TextSendMessage(text=text_))
                #
                # elif event.message.type == 'video':
                #     text_ = event.message.id
                #     message.append(TextSendMessage(text=text_))
                #
                # elif event.message.type == 'audio':
                #     text_ = event.message.id
                #     message.append(TextSendMessage(text=text_))
                #
                # elif event.message.type == 'location':
                #     text_ = event.message.id
                #     message.append(TextSendMessage(text=text_))

                # 回復傳入的訊息文字
                line_bot_api.reply_message( event.reply_token, message )

            # file_path = r'F:\AI\Line_Chatbot\django_chatbot'
            # image_content = line_bot_api.get_message_content(event.message.id)
            # image_name = os.path.join(file_path, "123.png")
            #
            # with open(image_name, 'wb') as fd:
            #     for chunk in image_content.iter_content():
            #         fd.write(chunk)

        return HttpResponse()
    else:
        return HttpResponseBadRequest()
