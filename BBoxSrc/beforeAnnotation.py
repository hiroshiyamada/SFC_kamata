# -*- coding: utf-8 -*-

import requests
import os
import sys
import cv2
from time import sleep
sys.path.append('../SFC_kamata/client')
import image_transform

# 画像のダウンロード


def download_image(url, timeout=10):
    # responseを取得
    response = requests.get(url, allow_redirects=False, timeout=timeout)
    return response.content

# 画像を連番にする


def make_filename(base_dir, number, url):
    # 拡張子を取得
    ext = os.path.splitext(url)[1]
    # 拡張子に番号を付ける
    filename = str(number) + ext
    # ファイル名でそのまま保存
    # filename = os.path.basename(url)
    # 画像の相対パスを作成
    relpath = os.path.join(base_dir, filename)
    return relpath

# 画像を保存する


def save_image(filename, image):
    with open(filename, "wb") as fout:
        fout.write(image)

# 画像ダウンロードメイン実行部


def getImage(num):
    # ラズパイで画像が保存されている場所
    url = "http://49.135.3.100/~pi/python/images/annotation/"
    # ジングルベルはクラス数9個のため、9種類の連番ディレクトリを作成する
    for i in range(10):
        # 画像の保存フォルダ名
        images_dir = "Images/" + "{:03}".format(i+1)
        os.makedirs(images_dir, exist_ok=True)
        # 取得画像のurl
        imageurl = url + num + ".jpg"
        # 元画像を保存するパス
        fileOrigin = "Images/original/" + num + ".jpg"
        # 変換後の画像を保存する相対パス
        filename = make_filename(images_dir, num, imageurl)
        # 画像をダウンロード
        image = download_image(imageurl)
        # 初回だけ元画像を保存
        if(i == 0):
            os.makedirs("Images/original", exist_ok=True)
            save_image(fileOrigin, image)
            print("saved original " + num + ".jpg in Images/original/")
        #グレイスケールで読み込み
        img = cv2.imread(fileOrigin, 0)
        # 歪み補正と直線補正
        img_tr = image_transform.image_transform(img)
        # 適応的2値化
        img_two = cv2.adaptiveThreshold(img_tr, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)
        img_two = cv2.cvtColor(img_two,cv2.COLOR_GRAY2RGB)
        #切り出し
        img_two = img_two[300:600, 200:600]
        #２倍に拡大
        img_two = cv2.resize(img_two, None, fx = 2, fy = 2)
        cv2.imwrite(filename, img_two)
        print("saved two value " + num + ".jpg in " + images_dir)


def postImageNum(num):
    postNum = {}
    postNum["key"] = num
    # マインドストームのアドレスに送信
    s = requests.session()
    r = s.post("http://49.135.3.100/~pi/python/receiveImageNum.py", data=postNum)
    # 送信結果を表示
    print(r.text)

# 画像撮影メイン実行部


def makeImage(num):
    url = "http://49.135.3.100/~pi/python/take_annotation.sh " + num
    print(url)
    # 画像を撮影
    requests.get(url, allow_redirects=False, timeout=10)


if __name__ == "__main__":
    postImageNum(sys.argv[1])
    getImage(sys.argv[1])
