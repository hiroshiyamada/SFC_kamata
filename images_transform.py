# coding:utf-8

import cv2
import numpy as np
import client.image_transform as tr

for i in range(15,25):
    #歪んだ画像読み込み
    img = cv2.imread('./images/'+ str(i) +'.jpg')
    img_tr = tr.image_transform(img)
    #変換した画像を保存する
    cv2.imwrite('images/transformed/' + str(i) + '.jpg', img_tr)
