# -*- coding: utf-8 -*-
import os
import sys
import signal
import cv2
sys.path.append(os.path.join(os.path.dirname(__file__), '../YOLO3-4-Py'))

import image
import move
import postData
import detectMusic
import imageYOLO
import image_transform

#楽譜を時系列で格納する配列
musicList = []
def handler(signal, frame):
    move.stop()
    sys.exit(0)

signal.signal(signal.SIGINT, handler)


#net = detectMusic.yoloNetwork()

N = 2
for i in range(N):
    print("i=", i)
    #ev3から画像を受信する
    image.makeImage()
    image.removeImage()
    image.getImage()
    if (i == 0):
        #動く
        move.move()
    if (i == N-1):
        #止まる
        move.stop()

    #グレイスケールで読み込む
    img = cv2.imread("images/0.jpg",0)
    #適応的2値化
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)
    img = cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)
    #座標変換
    img_tr = image_transform.image_transform(img)
    #img_tr = cv2.imread("/home/sfc_kamata/work/SFC_kamata/client/images/transformed/" + str(i+1) + ".jpg")
    #認識
    #detectionResults = detectMusic.yoloDetect_net(img_tr,net)
    detectionResults = detectMusic.yoloDetect(img_tr)
    print("detectionResults", detectionResults)
    #認識結果を楽譜形式に変換
    currentNote = imageYOLO.makeSound(detectionResults)
    print("currentNote", currentNote)
    #認識結果を表示
    detectMusic.writeBoundingBox(detectionResults, img_tr, i)
    if not detectionResults:
        #認識結果が空なら終了
        move.stop()
        break
    #新規楽譜の抽出 
    newNote = imageYOLO.findNewNotes(currentNote, musicList)
    #新規楽譜を結合
    musicList.extend(newNote)
    print("musicList",musicList)
#楽譜をev3に送信する
postData.postMusic(musicList)
