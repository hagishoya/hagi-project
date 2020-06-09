from flask import Flask,request,abort
from linebot import LineBotApi,WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent,TextMessage,TextSendMessage,ImageSendMessage
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
def handle_image(event):
    line_bot_api.reply_message(event.reply_token,ImageSendMessage(url = "https://www.google.com/imgres?imgurl=https%3A%2F%2Fimages-na.ssl-images-amazon.com%2Fimages%2FI%2F61OidffpzNL.jpg&imgrefurl=https%3A%2F%2Fwww.amazon.co.jp%2FBRUTUS-%25E3%2583%2596%25E3%2583%25AB%25E3%2583%25BC%25E3%2582%25BF%25E3%2582%25B9-2020%25E5%25B9%25B44-15%25E5%258F%25B7No-913-%25E7%258A%25AC%25E3%2581%258C%25E3%2581%2584%25E3%2581%25A6%25E3%2582%2588%25E3%2581%258B%25E3%2581%25A3%25E3%2581%259F%25E3%2580%2582%2Fdp%2FB085RQSYP3&tbnid=zLb7M0M3z3K6wM&vet=12ahUKEwiut5Ooy_PpAhUqEqYKHdpjDcYQMygAegUIARCfAg..i&docid=rFfgQ3trv06JMM&w=827&h=1118&q=%E7%8A%AC&ved=2ahUKEwiut5Ooy_PpAhUqEqYKHdpjDcYQMygAegUIARCfAg"))


if __name__=="__main__":
    port=int(os.getenv("PORT",5000))
    app.run(host="0.0.0.0",port=port)
