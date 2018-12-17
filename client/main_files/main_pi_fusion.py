# -*- coding: utf-8 -*-
import time
import image_transform
import imageYOLO
import postData
import postMoveData
import move
import image
import os
import sys
import signal
import cv2
import threading
import shutil

sys.path.append(os.path.join(os.path.dirname(__file__), '../YOLO3-4-Py'))
import detectMusic

# 時間計測開始
start_time = time.time()
print('TIME start time %f' % (time.time()-start_time))
# 楽譜を時系列で格納する配列
musicList = []


def handler(signal, frame):
    move.stop()
    sys.exit(0)


signal.signal(signal.SIGINT, handler)

print('TIME signal  %f' % (time.time()-start_time))
# networkの作成
net = detectMusic.yoloNetwork()
print('TIME network init  %f' % (time.time()-start_time))
# 画像を保存するディレクトリの削除
shutil.rmtree("images")
shutil.rmtree("output")
# ディレクトリの作成
os.mkdir("images")
os.mkdir("output")
#前回数字の保存
imageNum = 580
#前回認識結果の保存
pastNote=[]

N = 5000
for i in range(N):
    print('TIME i= %d %f' % (i,time.time()-start_time))
    #print('TIME image makeImage %f' % (time.time()-start_time))
    #ラズパイの画像を削除
    #image.removeImage()
    #print('TIME image remove %f' % (time.time()-start_time))
    if i ==0:
        print('TIME image getRecentPictureNum start %f' % (time.time()-start_time))
        recentNum = image.getRecentPictureNum()
        print('TIME image getRecentPictureNum %f' % (time.time()-start_time))
        imageNum = int(recentNum)
    while int(imageNum) > int(recentNum):
        #ラズパイから最新の一つ前の画像番号を取得
        print('TIME image getRecentPictureNum start %f' % (time.time()-start_time))
        recentNum = image.getRecentPictureNum()
        print('TIME image getRecentPictureNum %f' % (time.time()-start_time))
        print("recentNum = " + str(recentNum))
    #ラズパイから画像を取得
    print('TIME image getImage start %f' % (time.time()-start_time))
    image.getImage(str(imageNum).zfill(4))
    print('TIME image getImage %f' % (time.time()-start_time))
#    if (i == 0):
#        #動く
#        print('move')
#        move.move()
#        print('TIME move %f' % (time.time()-start_time))
##        pass # test
#    if (i == N-1):
#        #止まる
#        print('stop')
#        move.stop()
#        print('TIME stop %f' % (time.time()-start_time))
##        pass # test
    # グレイスケールで読み込む
    print('image read')
    print('offline imageNum', str(imageNum).zfill(4))
    img = cv2.imread("images/" + str(imageNum).zfill(4) + ".jpg")
    #img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    #img = cv2.imread(
    #    "/home/sfc_kamata/work/BBox-Label-Tool/Images/original/" + str(i+1) + ".jpg", 0)
    #print('TIME image read %f imageNum %d' % (time.time() - start_time, imageNum))
    # ２倍に拡大
    img_two = cv2.resize(img, None, fx = 2, fy = 2)
    # 認識
    detectionResults = detectMusic.yoloDetect_net(img_two, net)
    print('TIME detection %f' % (time.time()-start_time))
    #detectionResults = detectMusic.yoloDetect(img_two)
    print("detectionResults", detectionResults)
    postMoveData.post(detectionResults)
    print('TIME postMoveData %f' % (time.time()-start_time))
    # 認識結果を楽譜形式に変換
    currentNote = imageYOLO.makeSound(detectionResults)
    print('TIME currentNote %f' % (time.time()-start_time))
    print("currentNote", currentNote)
    # 認識結果を表示
    detectMusic.writeBoundingBox(detectionResults, img_two, int(imageNum))
    #print('TIME bounding box %f' % (time.time() - start_time))
    
    #if not detectionResults:
    #    # 認識結果が空なら終了
    #    move.stop()
    #    break
    # 新規楽譜の抽出
    newNote = imageYOLO.findNewNotes(currentNote, pastNote)
    pastNote = currentNote
    print('newNote %f' % (time.time()-start_time))
    print('offline cur',currentNote)
    print('offline new',newNote)
    # 新規楽譜を結合
    musicList.extend(newNote)
    print('TIME music list extend %f' % (time.time()-start_time))
    #楽譜をev3に送信する
    if newNote != []:
        postData.postMusic(newNote)
        #postData.postMusic_Christmas(newNote)
    #    pass  
    print('TIME postMusic%f' % (time.time()-start_time))
    print("musicList", musicList)
    # time.sleep(1.1)
    # imageNum += 18
    imageNum += 4

print('offline music',musicList)
#print('TIME music list send %f' % (time.time()-start_time))
