from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, ImageMessage, FlexSendMessage,CarouselContainer,BubbleContainer
import main
import json
import os
import cv2
import matplotlib.pyplot as plt
import numpy as np
import path_data


################################################################
###-------------------------イラスト--------------------------###

def illust_filter(img, K=20):

    # グレースケール変換
    gray = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)

    # ぼかしでノイズ低減
    edge = cv2.blur(gray, (3, 3))

    # Cannyアルゴリズムで輪郭抽出
    edge = cv2.Canny(edge, 50, 150, apertureSize=3)

    # 輪郭画像をRGB色空間に変換
    edge = cv2.cvtColor(edge, cv2.COLOR_GRAY2BGR)

    # 画像の減色処理
    img = np.array(img/K, dtype=np.uint8)
    img = np.array(img*K, dtype=np.uint8)

    # 差分を返す
    return cv2.subtract(img, edge)


def illust_image(event):
    
    image_path, output_path = path_data.get_image_path(event)

    # 元画像の読み込み
    img = cv2.imread(image_path)

    # 画像のアニメ絵化
    image = illust_filter(img, 30)

    # 結果出力
    cv2.imwrite(output_path, image)

################################################################