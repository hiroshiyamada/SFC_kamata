# -*- coding: utf-8 -*-
import os
import sys
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


for i in range(1):
    move.move()
    #ev3から画像を受信する
    image.getImage()
    img = cv2.imread("images/0.jpg")
    #座標変換
    img_tr = image_transform.image_transform(img)
    #img_tr = cv2.imread("/home/sfc_kamata/work/SFC_kamata/client/images/transformed/" + str(i+1) + ".jpg")
    #認識
    detectionResults = detectMusic.yoloDetect(img_tr)
    print("detectionResults", detectionResults)
    #認識結果を楽譜形式に変換
    currentNote = imageYOLO.makeSound(detectionResults)
    print("currentNote", currentNote)
    #認識結果を表示
    detectMusic.writeBoundingBox(detectionResults, img_tr)
    #新規楽譜の抽出 
    newNote = imageYOLO.findNewNotes(currentNote, musicList)
    #新規楽譜を結合
    musicList.extend(newNote)
    print("musicList",musicList)
    #楽譜をev3に送信する
    #postData.postMusic(musicList)
