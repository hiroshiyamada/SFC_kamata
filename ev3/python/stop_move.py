#!/usr/bin/python3
# -*- coding: utf-8 -*-

import ev3dev.ev3 as ev3
import time
import ev3dev.core
import cgitb; cgitb.enable()

def stop(motor_right,motor_left):
    motor_right.stop(stop_action='brake')
    motor_left.stop(stop_action='brake')        

#httpヘッダを出力
print("Content-Type: text/html\n\n")

#動かすモーターの指定
motor_left = ev3.LargeMotor('B')
motor_right = ev3.LargeMotor('C')
stop(motor_right,motor_left)

print("hoge")
