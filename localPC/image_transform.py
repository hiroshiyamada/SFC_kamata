#!/usr/bin/python2.7
# coding:utf-8

import cv2
import numpy as np

#キャリブレーション変数
dist = np.array([[ 0.05433881,  0.10537148,  0.00494094, -0.00717463, -0.34118259]])

mtx = np.array([[  1.39379573e+03,  0.00000000e+00, 5.83432701e+02],
       [  0.00000000e+00,   1.40024455e+03, 5.17751586e+02],
       [  0.00000000e+00,   0.00000000e+00, 1.00000000e+00]])

#歪んだ画像読み込み
img = cv2.imread('./image4.jpg')


cap = cv2.VideoCapture(0)
while(True):
    #画像を1フレーム読み込む
    #ret, img = cap.read()
    #歪み補正
    undist = cv2.undistort(img, mtx, dist, None, mtx)
    #画像のサイズを取得
    img_size = (img.shape[1], img.shape[0])
    
    #歪んでる画像で補正したい4点を手動で入力
    src = np.float32([[586, 300], [588, 525], [519, 525], [531, 300]])
    #真上から見たらこうなるだろうという理想の4点を手動で入力
    dst = np.float32([[586, 300], [586, 531], [524, 531], [524, 300]])
                
    #画像を真上に変換する行列を取得
    M = cv2.getPerspectiveTransform(src, dst)
    #真上から見た画像に変換する
    warped = cv2.warpPerspective(undist, M, img_size)
    cv2.imshow('image', warped)
    cv2.waitKey(1)
    #変換した画像を保存する
    cv2.imwrite('transformed.jpg', warped)
    break