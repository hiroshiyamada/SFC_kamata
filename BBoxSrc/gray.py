#!/usr/bin/python3
# -*- coding: utf-8 -*-

import cv2
import sys
import glob
import os

def main(cls_id):
    str_cls_id = "{:03}".format(cls_id+1)
    # 画像の読み込み
    files = glob.glob('./Images/increase/' + str_cls_id + '/*.jpg')

    for item_index, file_ in enumerate(files):
	#グレイスケールに変換
        img = cv2.imread(file_,0)
	######2値化学習画像トライ#########
        #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #cv2.merge((gray, gray, gray), img)
        #blur = cv2.GaussianBlur(img, (5,5), 0)
        #ret,img_otsu = cv2.threshold(blur,0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        #cv2.imwrite(file_, gray)
        #動的に閾値を決めて２値化
        img_adaptive = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)
        #cv2.imwrite("testaa.jpg",img_adaptive)
        #127以上は全て黒、それ以下は全て白
        #ret, img_thresh = cv2.threshold(img, 127, 255, cv2.THRESH_TOZERO)
        cv2.imwrite(file_,img_adaptive)

if __name__ == "__main__":
    for i in range(int(sys.argv[1])):
        main(i)


