# -*- coding: utf-8 -*-

import requests
import os
import sys
from time import sleep

#画像のダウンロード
def download_image(url, timeout = 10):
    #responseを取得
    response = requests.get(url, allow_redirects = False, timeout = timeout)
    return response.content

#画像を連番にする
def make_filename(base_dir, number, url):
    #拡張子を取得
    ext = os.path.splitext(url)[1]
    #拡張子に番号を付ける
    filename = str(number) + ext
    #ファイル名でそのまま保存
    #filename = os.path.basename(url)
    #画像の相対パスを作成
    relpath = os.path.join(base_dir, filename)
    return relpath

#画像を保存する
def save_image(filename, image):
    with open(filename, "wb") as fout:
        fout.write(image)

#画像ダウンロードメイン実行部
def getImage():
    #Mindstormで画像が保存されている場所
    url = "http://49.135.3.100/~pi/python/images/"
    #url = "http://49.135.3.100:8080/python/images/"
    #画像の保存フォルダ名
    images_dir = "images"
    #連番の番号(Todo:ここをループして連番にする?)
    num = 0
    #取得画像のurl
    imageurl = url + str(num) + ".jpg"
    #保存する画像の相対パス
    filename = make_filename(images_dir, num, imageurl)
    #画像をダウンロード
    image = download_image(imageurl)
    #画像を保存
    save_image(filename, image)
    print(num)
    num += 1
    sleep(1)

#画像撮影メイン実行部
def makeImage():
    url = "http://49.135.3.100/~pi/python/take_image.sh"
    #画像を撮影
    requests.get(url, allow_redirects = False, timeout = 10)

#画像を削除
def removeImage():
    #画像の保存フォルダ名
    images_dir = "images"
    #連番の番号(Todo:ここをループして連番にする?)
    num = 0
    #取得画像のurl
    imageurl = str(num) + ".jpg"
    #保存する画像の相対パス
    filename = make_filename(images_dir, num, imageurl)
    if (os.path.exists(filename)):
        os.remove(filename)

if __name__ == "__main__":
    removeImage()
