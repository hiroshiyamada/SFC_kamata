#!/usr/bin/python3
# -*- coding: utf-8 -*-

import ev3dev.ev3 as ev3
import time

motor_left = ev3.LargeMotor('outA')
motor_left.run_forever(speed_sp=500)
time.sleep(3)
motor_left.stop(stop_action='brake')

