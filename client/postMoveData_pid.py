# -*- coding: utf-8 -*-
import requests
from statistics import mean

#YOLOの認識結果を受け取る
'''
入力データの形式 results : [cat, score, bounds]
[(b'dog', 0.9993329048156738, (224.17959594726562, 378.47900390625, 178.75448608398438, 328.29620361328125)),
(b'bicycle', 0.991621732711792, (344.5289306640625, 286.759765625, 486.18890380859375, 321.3658447265625)), 
(b'truck', 0.9165929555892944, (580.9117431640625, 125.05439758300781, 208.13427734375, 87.27819061279297))]
'''
#クラス化
class MoveDataPost:
    #クラス変数で前回の差分を保存
    def __init__(self):
        self.pastXDiff = 0
        self.sumXDiff = 0
    def calcMotorSpeed(self, results):
        v0 = 87
        #v0 = 80
        xTarget = 400
        kp = 0.015
        ki = 0
        kd = 0
        xList = []
        for cat, score, bounds in results:
            #x,y:認識結果の中心のx座標とy座標, w,h:バウンディングボックスの横と縦の長さ
            x, y, w, h = bounds
            xList.append(x)
        if(xList == []):
            return v0, v0
        xave = mean(xList)
        print("DBG motor xave " + str(xave))
        print("DBG motor xDiff " + str(xave))
        print("DBG motor pastXDiff " + str(self.pastXDiff))
        print("DBG motor sumXDiff " + str(self.sumXDiff))
        #目標値との差分を計算
        xDiff = xTarget - xave
        #前回値との差分を計算
        prevDiff = xDiff - self.pastXDiff
        #これまでの差分の合計を計算
        self.sumXDiff = self.sumXDiff + xDiff
        #音符が左側にあるため、右側のモーター回転数を上げる
        if(xDiff > 0):
            motorRight = v0 + kp * xDiff + ki * self.sumXDiff + kd * prevDiff
            motorLeft = v0
        #音符が右側にあるため、左側のモーター回転数を上げる
        else:
            motorRight = v0 
            motorLeft = v0 - kp * xDiff - ki * self.sumXDiff - kd * prevDiff
        #過去値を保存する
        self.pastXDiff = prevDiff
        return int(motorRight), int(motorLeft)

    def post(self, results):
        '''
        motorSpeed = {}
        print("result : " + str(results))
        r, l = calcMotorSpeed(results)
        print("right : " + str(r))
        print("left : " + str(l))
        motorSpeed["right"] = r
        motorSpeed["left"] = l
        '''
        r, l = self.calcMotorSpeed(results)
        #motorSpeed =  str(r) + " " +str(l) 
        #s = requests.session()
        #r = s.post("http://49.135.3.100:8080/python/moveCorrectEV3_sh.py", data = motorSpeed)
        #送信結果を表示
        #print(r.text)
        return r, l
    
