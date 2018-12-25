#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os

# fswebcamを無限ループ（C-c中断等で実行失敗したら終了）
while(os.system("fswebcam -r 1280x720 images/0.jpg") == 0):
	pass
