#!/usr/bin/python3
# -*- coding: utf-8 -*-

import ev3dev.ev3 as ev3
import time
import ev3dev.core
import cgitb; cgitb.enable()

def Move(motor_right,motor_left,speed_right,speed_left):
    motor_right.run_forever(speed_sp=speed_right)
    motor_left.run_forever(speed_sp=speed_left)        

#httpヘッダを出力
print("Content-Type: text/html\n\n")

#動かすモーターの指定
motor_left = ev3.LargeMotor('B')
motor_right = ev3.LargeMotor('C')
t0 = time.time()
#print(motor_left.count_per_rot)
#
while(time.time()-t0 < 1):
    speed_right = 50
    speed_left = 50
    print("FOWARD!!!")
    Move(motor_right,motor_left,speed_right,speed_left)
t0 = time.time()
    
#while(time.time()-t0 < 5):
#    speed_right = 50
#    speed_left = 0
#    print("RIGHT!!!")
#    Move(motor_right,motor_left,speed_right,speed_left)
#t0 = time.time()
#
#while(time.time()-t0 < 5):
#    speed_right = 0
#    speed_left = 50
#    print("LEFT!!!")
#    Move(motor_right,motor_left,speed_right,speed_left)

motor_right.stop(stop_action='brake')
motor_left.stop(stop_action='brake')

print("hoge")
