# -*- coding: utf-8 -*-
import requests

def postMusic(notes):
    #入力データ
    test = {}
    #temp = []
    #test2 = [('D4', 'e3'),('D4', 'e3'),('D4', 'e3'),('G4', 'h'),('D5', 'h'),('C5', 'e3'),
    #('B4', 'e3'),('A4', 'e3'),('G5', 'h'),('D5', 'q'),('C5', 'e3'),('B4', 'e3'),
    #('A4', 'e3'),('G5', 'h'),('D5', 'q'),('C5', 'e3'),('B4', 'e3'),('C5', 'e3'),
    #('A4', 'h.')]
    #test2 = [('D4', 'e3'),('D4', 'e3'),('D4', 'e3'),('G4', 'h'),('D5', 'h'),('C5', 'e3')]

    test["key0"] = len(notes)
    for i in range(len(notes)):
        key = "key" + str(i+1)
        test[key] = notes[i]
        #temp.append(test2[i])
    #マインドストームのアドレスに送信
    s = requests.session()
    r = s.post("http://49.135.3.41/python/receive.py", data = test)
    #送信結果を表示
    print(r.text)
