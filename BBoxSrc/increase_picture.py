#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import cv2
import numpy as np
import sys
import glob
import os
import re
import numpy as np

# ヒストグラム均一化
def equalizeHistRGB(src):

    RGB = cv2.split(src)
    Blue   = RGB[0]
    Green = RGB[1]
    Red    = RGB[2]
    for i in range(3):
        cv2.equalizeHist(RGB[i])

    img_hist = cv2.merge([RGB[0],RGB[1], RGB[2]])
    return img_hist

# ガウシアンノイズ
def addGaussianNoise(src):
    row,col,ch= src.shape
    mean = 0
    var = 0.1
    sigma = 15
    gauss = np.random.normal(mean,sigma,(row,col,ch))
    gauss = gauss.reshape(row,col,ch)
    noisy = src + gauss

    return noisy

# salt&pepperノイズ
def addSaltPepperNoise(src):
    row,col,ch = src.shape
    s_vs_p = 0.5
    amount = 0.004
    out = src.copy()
    # Salt mode
    num_salt = np.ceil(amount * src.size * s_vs_p)
    coords = [np.random.randint(0, i-1 , int(num_salt))
              for i in src.shape]
    out[coords[:-1]] = (255,255,255)

    # Pepper mode
    num_pepper = np.ceil(amount* src.size * (1. - s_vs_p))
    coords = [np.random.randint(0, i-1 , int(num_pepper))
              for i in src.shape]
    out[coords[:-1]] = (0,0,0)
    return out

def main(cls_id):
    str_cls_id = "{:03}".format(cls_id+1)
    # ルックアップテーブルの生成
    min_table = 50
    max_table = 205
    diff_table = max_table - min_table
    gamma1 = 0.75
    gamma2 = 1.5

    LUT_HC = np.arange(256, dtype = 'uint8' )
    LUT_LC = np.arange(256, dtype = 'uint8' )
    LUT_G1 = np.arange(256, dtype = 'uint8' )
    LUT_G2 = np.arange(256, dtype = 'uint8' )

    LUTs = []

    # 平滑化用
    average_square = (10,10)

    # ハイコントラストLUT作成
    for i in range(0, min_table):
        LUT_HC[i] = 0

    for i in range(min_table, max_table):
        LUT_HC[i] = 255 * (i - min_table) / diff_table

    for i in range(max_table, 255):
        LUT_HC[i] = 255

    # その他LUT作成
    for i in range(256):
        LUT_LC[i] = min_table + i * (diff_table) / 255
        LUT_G1[i] = 255 * pow(float(i) / 255, 1.0 / gamma1)
        LUT_G2[i] = 255 * pow(float(i) / 255, 1.0 / gamma2)

    LUTs.append(LUT_HC)
    LUTs.append(LUT_LC)
    LUTs.append(LUT_G1)
    LUTs.append(LUT_G2)

    # 画像の読み込み
    files = glob.glob('./Images/' + str_cls_id + '/*.jpg')

    for item_index, file in enumerate(files):
        img_src = cv2.imread(file, 1)

        trans_img = []
        trans_img.append(img_src)

        # LUT変換
        for i, LUT in enumerate(LUTs):
            trans_img.append( cv2.LUT(img_src, LUT))

        # 平滑化
        trans_img.append(cv2.blur(img_src, average_square))

        # ヒストグラム均一化
        trans_img.append(equalizeHistRGB(img_src))

        # ノイズ付加
        trans_img.append(addGaussianNoise(img_src))
        trans_img.append(addSaltPepperNoise(img_src))

        # 反転
        flip_img = []
        for img in trans_img:
            flip_img.append(cv2.flip(img, 1))
        trans_img.extend(flip_img)

        # 保存
        if not os.path.exists("training_images"):
            os.mkdir("training_images")

        base = os.path.splitext(os.path.basename(file))[0] + "_"
        item_txt = os.path.splitext(os.path.basename(file))[0] + '.txt'
        img_src.astype(np.float64)
        for i, img in enumerate(trans_img):
            # 比較用
            # cv2.imwrite("target_images/" + base + str(i) + ".jpg" ,cv2.hconcat([img_src.astype(np.float64), img.astype(np.float64)]))
            #9以下は反転していない
            coordinate = ''
            file = open("./Labels/" + str_cls_id + "/" + item_txt, 'r')
            if i <= 8:
                coordinate = file.read()
            #9以上は反転している
            else:
                line = file.readline()
                coordinate = line

                while line:
                    line = file.readline()
                    words = re.split(" +", line)
                    if len(words) >= 2:
                        x = words[0]
                        y = words[1]
                        width = words[2]
                        height = words[3]
                        img_width = img.shape[1]

                        x = int(img_width) - int(width)
                        width = int(img_width) - int(words[0])

                        coordinate = coordinate + ' '.join([
                            str(x).strip(),
                            str(y).strip(),
                            str(width).strip(),
                            str(height).strip()
                        ]) + '\n'

            file.close()

            f = open("training_images/" + str_cls_id + "/" + base + str(i) + ".txt", 'w')
            f.write(coordinate)
            f.close()

            cv2.imwrite("Images/increase/" + str_cls_id + "/" + base + str(i) + ".jpg" ,img)

if __name__ == '__main__':
    for i in range(int(sys.argv[1])):
        main(i)