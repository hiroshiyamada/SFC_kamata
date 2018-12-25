#!/bin/bash
#moto 80
echo 40 > /sys/class/tacho-motor/motor0/speed_sp
echo 40 > /sys/class/tacho-motor/motor1/speed_sp
echo run-forever > /sys/class/tacho-motor/motor0/command
echo run-forever > /sys/class/tacho-motor/motor1/command
