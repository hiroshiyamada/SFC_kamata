# coding:utf-8

import cv2
import numpy as np
#import matplotlib.pyplot as plt
#from time import sleep

#キャリブレーション変数
dist = np.array([[ 0.05433881,  0.10537148,  0.00494094, -0.00717463, -0.34118259]])

mtx = np.array([[  1.39379573e+03,  0.00000000e+00, 5.83432701e+02],
       [  0.00000000e+00,   1.40024455e+03, 5.17751586e+02],
       [  0.00000000e+00,   0.00000000e+00, 1.00000000e+00]])

def image_transform(img):
    #歪んだ画像読み込み
    #img = cv2.imread('./images/'+ str(img_count) +'.jpg')
    #cv2.imshow("b",img)
    #歪み補正
    undist = cv2.undistort(img, mtx, dist, None, mtx)
    #画像のサイズを取得
    img_size = (img.shape[1], img.shape[0])
    
    #歪んでる画像で補正したい4点を手動で入力
    src = np.float32([[586, 300], [588, 525], [519, 525], [531, 300]])
    src = src/1.5
    #真上から見たらこうなるだろうという理想の4点を手動で入力
    dst = np.float32([[590, 300], [590, 531], [527, 531], [527, 300]])
                
    #画像を真上に変換する行列を取得
    M = cv2.getPerspectiveTransform(src, dst)
    #真上から見た画像に変換する
    warped = cv2.warpPerspective(undist, M, img_size)

    #変換した画像を保存する
    #cv2.imwrite('images/transformed/' + str(img_count) + '.jpg', warped)

    return warped

'''
#cap = cv2.VideoCapture(1)
img_count =1
while(img_count < 15):
    #歪んだ画像読み込み
    img = cv2.imread('./images/'+ str(img_count) +'.jpg')
    #img = cv2.imread('./images/image4.jpg')
    #img = cv2.imread('./images/test.jpg')
    #画像を1フレーム読み込む
    #ret, img = cap.read()
    cv2.imshow("b",img)
    #plt.imshow(img)
    #cv2.imwrite('raw_image.jpg', img)
    #歪み補正
    undist = cv2.undistort(img, mtx, dist, None, mtx)
    #画像のサイズを取得
    img_size = (img.shape[1], img.shape[0])
    
    #歪んでる画像で補正したい4点を手動で入力
    src = np.float32([[586, 300], [588, 525], [519, 525], [531, 300]])
    src = src/1.5
    plt.plot(586/2, 300/2, '.')
    plt.plot(588/2, 525/2, '.')
    plt.plot(519/2, 525/2, '.')
    plt.plot(531/2, 300/2, '.')
    #真上から見たらこうなるだろうという理想の4点を手動で入力
    dst = np.float32([[590, 300], [590, 531], [527, 531], [527, 300]])
    dst = dst
                
    #画像を真上に変換する行列を取得
    M = cv2.getPerspectiveTransform(src, dst)
    #真上から見た画像に変換する
    warped = cv2.warpPerspective(undist, M, img_size)
    cv2.imshow("a",warped)
    #plt.imshow(warped)
    plt.plot(590/2, 300/2, '.')
    plt.plot(590/2, 531/2, '.')
    plt.plot(527/2, 531/2, '.')
    plt.plot(527/2, 300/2, '.')

    #cv2.waitKey(1)
    #plt.show()
    #変換した画像を保存する
    cv2.imwrite('images/transformed/' + str(img_count) + '.jpg', warped)
    img_count += 1;
    #break
'''
