#!/usr/bin/python3
import cv2
import time
import os
import shutil
import image_transform

start = time.time()
target_dir = 'images'
shutil.rmtree(target_dir)
os.mkdir(target_dir)
cap = cv2.VideoCapture(0)
k = 0

while True :
    print('cap %f' %(time.time() - start))
    ret, frame = cap.read()
    img = cv2.resize(frame , dsize=(800, 600))
    #グレイスケールに変換
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #####
    # 歪み補正と直線補正
    if img is None:
        print('image is None!')
        break
    else:
        img_tr = image_transform.image_transform(img)
    # 適応的2値化
    img_two = cv2.adaptiveThreshold(
        img_tr, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    # 切り出し
    img_two = img_two[300:600, 200:600]
    #####
    k_str = str(k).zfill(4)
    name = "images/" + k_str + ".jpg"
    cv2.imwrite(name, img_two)
    k = k + 1
    #cv2.waitKey(100)
    if (k > 3000):
        break
cap.release()
