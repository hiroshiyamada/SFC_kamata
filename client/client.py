# -*- coding: utf-8 -*-

import requests
import os
import sys

response = requests.get("http://49.135.3.41/python/test.py");
print(response.text);

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
    filename = number + ext
    #ファイル名でそのまま保存
    #filename = os.path.basename(url)
    #画像の相対パスを作成
    relpath = os.path.join(base_dir, filename)
    return relpath

#画像を保存する
def save_image(filename, image):
    with open(filename, "wb") as fout:
        fout.write(image)

#メイン実行部
if __name__ == "__main__":
    #Mindstormで画像が保存されている場所
    url = "http://49.135.3.41/python/images/test.jpg"
    #連番の番号(Todo:ここをループして連番にする?)
    num = "1"
    #画像の保存フォルダ名
    images_dir = "images"
    #保尊する画像の相対パス
    filename = make_filename(images_dir, num, url)
    #画像をダウンロードaaa
    image = download_image(url)
    #画像を保存
    save_image(filename, image)