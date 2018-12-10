# -*- coding: utf-8 -*-
import time
import image_transform
import imageYOLO
import postData
import move
import image
import os
import sys
import signal
import cv2
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
# ラズパイへ画像キャプチャ指示
#image.makeImage()

N = 7
for i in range(N):
    '''
    print("i=", i)
    # ev3から画像を受信する
    #image.makeImage()
    #print('image makeImage %f' % (time.time()-start_time))
    #image.removeImage()
    print('image remove %f' % (time.time()-start_time))
    #image.getImage()
    print('image getImage %f' % (time.time()-start_time))
    """
    if (i == 0):
        #動く
        move.move()
    if (i == N-1):
        #止まる
        move.stop()
    """
    '''
    # グレイスケールで読み込む
    #img = cv2.imread("images/0.jpg",0)
    img = cv2.imread(
        "/home/sfc_kamata/work/BBox-Label-Tool/Images/original/test_" + str(i+1) + ".jpg", 0)
    print('image read %f' % (time.time() - start_time))
    # 歪み補正と直線補正
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
    print('detection %f' % (time.time()-start_time))
    #detectionResults = detectMusic.yoloDetect(img_two)
    print("detectionResults", detectionResults)
    # 認識結果を楽譜形式に変換
    currentNote = imageYOLO.makeSound(detectionResults)
    print('currentNote %f' % (time.time()-start_time))
    print("currentNote", currentNote)
    # 認識結果を表示
    detectMusic.writeBoundingBox(detectionResults, img_two, i)
    print('bounding box %f' % (time.time() - start_time))
    '''
    if not detectionResults:
        # 認識結果が空なら終了
       # move.stop()
        break
    '''
    # 新規楽譜の抽出
    newNote = imageYOLO.findNewNotes(currentNote, musicList)
    print('newNote %f' % (time.time()-start_time))
    # 新規楽譜を結合
    musicList.extend(newNote)
    #楽譜をev3に送信する
    #if newNote != []:
    #    postData.postMusic(newNote)
    #print('music list extend %f' % (time.time()-start_time))
    #print("musicList", musicList)
#print('music list send %f' % (time.time()-start_time))
