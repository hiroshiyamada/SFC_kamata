#!/usr/bin/python3
# -*- coding: utf-8 -*-

import ev3dev.ev3 as ev3
import time
import ev3dev.core
import threading

#qを入力したら止まる
flag_quit = False
def quit_input():
    if(input() == "q"):
        flag_quit = True

#SFCの紹介をしゃべる
def speakSFC():
    ev3dev.core.Sound.set_volume(100)
    ev3dev.core.Sound.speak('Welcome to our S F C Kamata project!').wait()
    #ev3.Sound.speak('I am going to play a music song. Have Fun!').wait()

def Move(motor_right,motor_left,speed_right,speed_left):
    motor_right.run_forever(speed_sp=speed_right)
    motor_left.run_forever(speed_sp=speed_left)        

#自己紹介文をしゃべる
speakSFC()
#入力受付スレッドを開始
thread1 = threading.Thread(target=quit_input)
thread1.start()
#動かすモーターの指定
motor_left = ev3.LargeMotor('B')
motor_right = ev3.LargeMotor('C')
t0 = time.time()
print(motor_left.count_per_rot)
#
while(time.time()-t0 < 30):
    speed_right = 150
    speed_left = 150
    print("FOWARD!!!")
    Move(motor_right,motor_left,speed_right,speed_left)
t0 = time.time()
    
while(time.time()-t0 < 5):
    speed_right = 50
    speed_left = 0
    print("RIGHT!!!")
    Move(motor_right,motor_left,speed_right,speed_left)
t0 = time.time()

while(time.time()-t0 < 5):
    speed_right = 0
    speed_left = 50
    print("LEFT!!!")
    Move(motor_right,motor_left,speed_right,speed_left)

motor_right.stop(stop_action='brake')
motor_left.stop(stop_action='brake')

