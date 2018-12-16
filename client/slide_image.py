# -*- coding: utf-8 -*-
import image_transform
import image
import os
import sys
import signal
import cv2

# グレイスケールで読み込む
raw = cv2.imread("slide_image/3.jpg",0)
cv2.imwrite("slide_image/raw.jpg",raw)
# 歪み補正と直線補正
warp = image_transform.image_transform(raw)
cv2.imwrite("slide_image/warp.jpg",warp)
# 切り出し
cut = warp[300:600, 200:600]
cv2.imwrite("slide_image/cut.jpg",cut)
# ２倍に拡大
enlarge = cv2.resize(cut, None, fx = 2, fy = 2)
cv2.imwrite("slide_image/enlarge.jpg",enlarge)
# 適応的2値化
binary = cv2.adaptiveThreshold(
enlarge, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
binary = cv2.cvtColor(binary, cv2.COLOR_GRAY2RGB)
cv2.imwrite("slide_image/binary.jpg",binary)
