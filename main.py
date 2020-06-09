from flask import Flask,request,abort
from linebot import LineBotApi,WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent,TextMessage,TextSendMessage,ImageSendMessage,ImageMessage
import os

app=Flask(__name__)

YOUR_CHANNEL_ACCESS_TOKEN="rl1NmaTQR7jCWwiRmTGxq/6qVAB08MXr97h0a3FiTp4yo/yyPIdBfDI2aDUEuoZOGDnIS5ujoAtsNG7eEW5V4QDgIQSuL892yo0vLbELt9OSliCUu0iJG4dqzRQwOtzxImdNfMAO+D8JWcxZS8fntgdB04t89/1O/w1cDnyilFU="
YOUR_CHANNEL_SECRET="9f66f5b734e9db071bf0a5c535429bf4"
line_bot_api=LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler=WebhookHandler(YOUR_CHANNEL_SECRET)

@app.route("/callback",methods=["POST"])
def callback():
    signature=request.headers["X-Line-Signature"]

    body=request.get_data(as_text=True)
    app.logger.info("Request body"+body)

    try:
        handler.handle(body,signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"

@handler.add(MessageEvent,message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(event.reply_token,
                               [
                                   TextSendMessage(text=event.message.text),
                                   TextSendMessage(text="おつかれさまです。"),
                                ]
                               )
@handler.add(MessageEvent,message=ImageMessage)
def handle_image(event):
    line_bot_api.reply_message(event.reply_token,ImageSendMessage(
        original_content_url="https://www.min-petlife.com/data/article/239797/main_239797_cd32b_detail.jpg",
        preview_image_url="https://dol.ismcdn.jp/mwimgs/7/1/670m/img_71c53c1d81500a1cf73a4f543e72413f27838.jpg"
    ))
if __name__=="__main__":
    port=int(os.getenv("PORT",5000))
    app.run(host="0.0.0.0",port=port)
