from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, ImageMessage, FlexSendMessage,CarouselContainer,BubbleContainer
import json
import os
import cv2


app = Flask(__name__)

YOUR_CHANNEL_ACCESS_TOKEN = "rl1NmaTQR7jCWwiRmTGxq/6qVAB08MXr97h0a3FiTp4yo/yyPIdBfDI2aDUEuoZOGDnIS5ujoAtsNG7eEW5V4QDgIQSuL892yo0vLbELt9OSliCUu0iJG4dqzRQwOtzxImdNfMAO+D8JWcxZS8fntgdB04t89/1O/w1cDnyilFU="
YOUR_CHANNEL_SECRET = "9f66f5b734e9db071bf0a5c535429bf4"
line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)
FQDN = "https://project-hagi.herokuapp.com"


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]

    body = request.get_data(as_text=True)
    print("Request body" + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(event.reply_token,
       [
           TextSendMessage(text=event.message.text),
           #TextSendMessage(text="おはよ------"),
           #TextSendMessage(text="顔、目を検知できませんでした。"),
           #TextSendMessage(text=event.message.id),
       ]
       )


def handle_textmessage(event):
    line_bot_api.reply_message(event.reply_token,
        [
            #TextSendMessage(text=event.message.text),
            TextSendMessage(text="顔、目を検知できませんでした。"),
            #TextSendMessage(text=event.message.id),
        ]
        )

#おうむ返しコード
# @handler.add(MessageEvent,message=ImageMessage)
# def handle_image(event):
#    line_bot_api.reply_message(
#        event.reply_token,ImageSendMessage(
#        original_content_url="https://dol.ismcdn.jp/mwimgs/6/1/670m/img_71c53c1d81500a1cf73a4f543e72413f27838.jpg",
#        preview_image_url="https://www.min-petlife.com/data/article/239797/main_239797_cd32b_detail.jpg",
#        )
#    )


@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    print("メッセージID")
    print(event.message.id)
    message_content = line_bot_api.get_message_content(event.message.id)
    if not os.path.exists('static'):
        os.mkdir('static/')
    with open("static/" + event.message.id + ".jpg", "wb") as f:
        f.write(message_content.content)
    
    #json_open = open('hello.json', 'r')
    #json_load = json.load(json_open)
    #print(json_load)
    #new_from_json_dictメソッドはJSONデータをFlexMessage等各種オブジェクトに変換してくれるメソッドです
    #FlexSendMessage.new_from_json_dict(対象のJSONデータ）とすることで、
    #FlexSendMessage型に変換されます
    #container_obj = FlexSendMessage.new_from_json_dict(hello.payload)

    #最後に、push_messageメソッドを使ってPUSH送信する
    #line_bot_api.push_message('U69acb65348d94ebce854dd5cb9bf4840', messages=container_obj)
    flex(event)
    result = change_image(event)

        #mozaiku(event)



    if result:
        line_bot_api.reply_message(
            event.reply_token, ImageSendMessage(
                original_content_url=FQDN + "/static/" + event.message.id + "_face.jpg",
                preview_image_url=FQDN + "/static/" + event.message.id + "_face.jpg",
            )
        )

    else:
        handle_textmessage(event)

@handler.add(MessageEvent)
def flex(event):
    json_open = open('hello.json', 'r')
    line_bot_api.reply_message(
        event.reply_token,
        FlexSendMessage(
            alt_text="flex",
            contents=BubbleContainer.new_from_json_dict(json.loads(json_open))
        )
    )
    #line_bot_api.push_message("U69acb65348d94ebce854dd5cb9bf4840", messages=select__theme_massage) 

#囲う処理
def change_image(event):
    bool = True
    cascade_path = "haarcascade_frontalface_default.xml"
    cascade_eye_path = "haarcascade_eye.xml"

    image_file = event.message.id + ".jpg"
    save_file = event.message.id + "_face.jpg"
    #save_file2 = event.message.id + "_face2.jpg"
    print("イメージファイル: {} // {}".format(image_file, save_file))
    image_path = "static/" + image_file
    print("イメージパス: {}".format(image_path))
    output_path = "static/" + save_file
    #output_path2 = "static/" + save_file2
    print("アウトプットパス: {}".format(output_path))
    # ファイル読み込みo
    image = cv2.imread(image_path)

    # グレースケール変換
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # カスケード分類器の特徴量を取得する
    cascade = cv2.CascadeClassifier(cascade_path)
    cascade_eye = cv2.CascadeClassifier(cascade_eye_path)
    # 物体認識（顔認識）の実行
    # image – CV_8U 型の行列．ここに格納されている画像中から物体が検出されます
    # objects – 矩形を要素とするベクトル．それぞれの矩形は，検出した物体を含みます
    # scaleFactor – 各画像スケールにおける縮小量を表します
    # minNeighbors – 物体候補となる矩形は，最低でもこの数だけの近傍矩形を含む必要があります
    # flags – このパラメータは，新しいカスケードでは利用されません．古いカスケードに対しては，cvHaarDetectObjects 関数の場合と同じ意味を持ちます
    # minSize – 物体が取り得る最小サイズ．これよりも小さい物体は無視されます
    facerect = cascade.detectMultiScale(image_gray, scaleFactor=1.1, minNeighbors=2, minSize=(30, 30))
    eyerect = cascade_eye.detectMultiScale(image_gray, scaleFactor=1.1, minNeighbors=2, minSize=(20, 20))
    print("レクト:{} // {}".format(facerect, eyerect))
    print("ぎっとぽっど")

    color = (255, 0, 0)  # 青

    ## 検出した場合
    #if len(facerect) > 0:
    #    # 検出した顔を囲む矩形の作成
    #    for rect in facerect:
    #        cv2.rectangle(image, tuple(rect[0:2]), tuple(rect[0:2] + rect[2:4]), color, thickness=1)
    #        print(facerect)
    #        print(rect)
    #else:
    #    bool = False

    ratio = 0.05  # 縮小処理時の縮小率(小さいほどモザイクが大きくなる)
    if len(eyerect) > 0:
        # for rect in eyerect:
        #     cv2.rectangle(image, tuple(rect[0:2]), tuple(rect[0:2] + rect[2:4]), color, thickness=1)
        #     print(eyerect)
        #     print(rect)
           

        for x, y, w, h in eyerect:  # 引数でeyesで取得した数分forループ
           # y:はHEIGHT、x:はWEIGHT  fxはxの縮小率、fyはyの縮小率
           small = cv2.resize(image[y: y + h, x: x + w], None, fx=ratio, fy=ratio, interpolation=cv2.INTER_NEAREST)
           image[y: y + h, x: x + w] = cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)
           
    else:
        bool = False

    if bool:
        # 認識結果の保存
        cv2.imwrite(output_path, image)
        #cv2.imwrite(output_path2, image)
        return True
    else:
        return False


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
