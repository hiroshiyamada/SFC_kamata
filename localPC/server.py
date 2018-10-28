#!/usr/bin/python3
# -*- coding: utf-8 -*-

import socket
import pickle
from time import sleep

import sound

# パラメータ
port = 8000

class Server():
    def __init__(self):
        self.server = socket.socket()
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(('', port))
        self.server.listen(1)
        print("listen")
        self.client, addr = self.server.accept()
        print("accept")

    def send_loop(self):
        music = sound.get_music();
        for tone in music:
            sleep(0.01)
            b = pickle.dumps(tone)
            self.client.send(b)
        self.client.send(b"end")

if __name__ == "__main__":
    s = Server()
    try:
        s.send_loop()
    finally:
        s.client.close()
        s.server.close()
        print("close")
