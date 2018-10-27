# -*- coding: utf-8 -*-
import requests

#入力データ
test = {"key" : "hogehoge"}
#マインドストームのアドレスに送信
s = requests.session()
r = s.post("http://49.135.3.41/python/receive.py", data = test)
#送信結果を表示
print(r.text)