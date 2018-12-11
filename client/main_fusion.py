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
print('start time %f' % (time.time()-start_time))
# 楽譜を時系列で格納する配列
musicList = []


def handler(signal, frame):
    move.stop()
    sys.exit(0)


signal.signal(signal.SIGINT, handler)

print('signal  %f' % (time.time()-start_time))
# networkの作成
net = detectMusic.yoloNetwork()
print('network init  %f' % (time.time()-start_time))
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

N = 100
for i in range(N):
    print("offline i=", i)
    #print('image makeImage %f' % (time.time()-start_time))
    #ラズパイの画像を削除
    #image.removeImage()
    #print('image remove %f' % (time.time()-start_time))
    if i ==0:
        recentNum = image.getRecentPictureNum()
        imageNum = int(recentNum)
    while int(imageNum) > int(recentNum):
        #ラズパイから最新の一つ前の画像番号を取得
        recentNum = image.getRecentPictureNum()
        print("recentNum = " + str(recentNum))
    #ラズパイから画像を取得
    image.getImage(str(imageNum).zfill(4))
    print('image getImage %f' % (time.time()-start_time))
    if (i == 0):
        #動く
        print('move')
        #move.move()
        print('move %f' % (time.time()-start_time))
#        pass # test
    if (i == N-1):
        #止まる
        print('stop')
        move.stop()
        print('stop %f' % (time.time()-start_time))
#        pass # test
    # グレイスケールで読み込む
    print('image read')
    print('offline imageNum', str(imageNum).zfill(4))
    img = cv2.imread("images/" + str(imageNum).zfill(4) + ".jpg",0)
    #img = cv2.imread(
    #    "/home/sfc_kamata/work/BBox-Label-Tool/Images/original/" + str(i+1) + ".jpg", 0)
    print('image read %f imageNum %d' % (time.time() - start_time, imageNum))
    # 歪み補正と直線補正
    if img is None:
        print('image is None!')
        break
    else:
        img_tr = image_transform.image_transform(img)
    print('transform %f' % (time.time()-start_time))
    # 適応的2値化
    img_two = cv2.adaptiveThreshold(
        img_tr, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    img_two = cv2.cvtColor(img_two, cv2.COLOR_GRAY2RGB)
    print('cvt color %f' % (time.time()-start_time))
    # 切り出し
    img_two = img_two[300:600, 200:600]
    # ２倍に拡大
    img_two = cv2.resize(img_two, None, fx = 2, fy = 2)
    # 認識
    detectionResults = detectMusic.yoloDetect_net(img_two, net)
#    detectionResults = [(b'u_do', 0.9993329048156738, (224.17959594726562, 378.47900390625, 178.75448608398438, 328.29620361328125))] # test
    print('detection %f' % (time.time()-start_time))
    #detectionResults = detectMusic.yoloDetect(img_two)
    print("detectionResults", detectionResults)
    postMoveData.post(detectionResults)
    # 認識結果を楽譜形式に変換
    currentNote = imageYOLO.makeSound(detectionResults)
    print('currentNote %f' % (time.time()-start_time))
    print("currentNote", currentNote)
    # 認識結果を表示
    detectMusic.writeBoundingBox(detectionResults, img_two, int(imageNum))
    #print('bounding box %f' % (time.time() - start_time))
    
#    if not detectionResults:
#        # 認識結果が空なら終了
#        move.stop()
#        break
    # 新規楽譜の抽出
    newNote = imageYOLO.findNewNotes(currentNote, pastNote)
    pastNote = currentNote
    print('newNote %f' % (time.time()-start_time))
    print('offline cur',currentNote)
    print('offline new',newNote)
    # 新規楽譜を結合
    musicList.extend(newNote)
    #楽譜をev3に送信する
    #if newNote != []:
    #    #postData.postMusic(newNote)
    #    pass
    postData.postMusic(newNote)
    print('music list extend %f' % (time.time()-start_time))
    print("musicList", musicList)
#    time.sleep(1.1)
#    imageNum += 18
    imageNum += 8 

print('offline music',musicList)
#print('music list send %f' % (time.time()-start_time))
