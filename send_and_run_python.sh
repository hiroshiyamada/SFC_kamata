#!/bin/sh

scp $1 robot@${ip_ev3}:/home/robot/
ssh robot@${ip_ev3} python3 $1
