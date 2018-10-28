#!/usr/bin/python3
# -*- coding: utf-8 -*-

#!/usr/bin/python3
# -*- coding: utf-8 -*-

import queue
import threading
import socket
import pickle
from time import sleep
import cv2

import sound

# パラメータ
port = 8000

#カメラ画像を取得
cap = cv2.VideoCapture(0)

# global
recv_queue = queue.Queue()
finish_recv = False

class  RecvThread(threading.Thread):
    def __init__(self):
        super(RecvThread, self).__init__()
        self.client = socket.socket()
        self.client.connect(("localhost", port))


    def run(self):
        global finish_recv
        while True:
            try:
                recv_data = self.client.recv(2048)
            except:
                break
            if recv_data == b"end":
                break
            tone = pickle.loads(recv_data)
            recv_queue.put(tone)
        finish_recv = True
        print("finish recv")

class  SoundThread(threading.Thread):
    def __init__(self):
        super(SoundThread, self).__init__()

    def run(self):
        global finish_recv
        count = 0
        while True:
            if recv_queue.empty():
                if finish_recv:
                    break
                else:
                    continue
            tone = recv_queue.get()
            print(tone)
            count += 1
            print(count)
            sleep(0.02)
        print("finish sound")

if __name__ == "__main__":
    ts = SoundThread()
    tr = RecvThread()
    ts.start()
    tr.start()
    ts.join()
    tr.join()



cap = cv2.VideoCapture(0)

ret, frame = cap.read()

