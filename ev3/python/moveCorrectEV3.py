#!/usr/bin/python3
# -*- coding: utf-8 -*-

import ev3dev.ev3 as ev3
import cgi
import ev3dev.core
import cgitb; cgitb.enable()

def Move(motor_right,motor_left,speed_right,speed_left):
    motor_right.run_forever(speed_sp=int(speed_right))
    motor_left.run_forever(speed_sp=int(speed_left))        

form = cgi.FieldStorage()
print("Content-Type: text/html\n\n")

#動かすモーターの指定
motor_left = ev3.LargeMotor('B')
motor_right = ev3.LargeMotor('C')

speedRight = form.getvalue("right")
speedLeft = form.getvalue("left")
print("Right Speed : " + str(speedRight))
print("Left Speed : " + str(speedLeft))
print("test")
Move(motor_right,motor_left,speedRight,speedLeft)
