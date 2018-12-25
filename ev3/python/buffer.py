#!/usr/bin/python3
# -*- coding: utf-8 -*-

import queue
import threading
from time import sleep

# パラメータ
port = 8000
localpc_ip = "localhost"

# global
recv_queue = queue.Queue()
finish_recv = False

class  ReadThread(threading.Thread):
    def __init__(self):
        super(ReadThread, self).__init__()


    def run(self):
        global finish_recv
        while True:
            f = open("test.fifo", "r")
            for line in f:
                if line == "end\n":
                    finish_recv = True
                    #print("finish recv")
                    return
                recv_queue.put(line)
            f.close()

class  WriteThread(threading.Thread):
    def __init__(self):
        super(WriteThread, self).__init__()

    def run(self):
        global finish_recv
        while True:
            if recv_queue.empty():
                if finish_recv:
                    break
                else:
                    sleep(0.01)
                    continue
            tone = recv_queue.get()
            print(tone, flush=True)
        #print("finish sound")

def main():
    #print("start main")
    ts = WriteThread()
    tr = ReadThread()
    ts.start()
    tr.start()
    ts.join()
    tr.join()

if __name__ == "__main__":
    main()
