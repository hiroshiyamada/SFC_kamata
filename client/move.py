# -*- coding: utf-8 -*-

import requests

#GETリクエストを送る
def request_get(url, timeout = 10):
    #responseを取得
    response = requests.get(url, allow_redirects = False, timeout = timeout)
    return response.content

#メイン実行部
def move():
    #Mindstormで移動プログラムが保存されている場所
    url = "http://49.135.3.41/python/move.py"
    
    ret = request_get(url, 10000)
    print(ret)
