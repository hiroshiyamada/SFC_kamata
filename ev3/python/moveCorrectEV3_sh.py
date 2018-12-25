#!/bin/bash

echo "Content-type: text/html"
echo ""
read r l
echo $r > /sys/class/tacho-motor/motor0/speed_sp
echo $l > /sys/class/tacho-motor/motor1/speed_sp
echo run-forever > /sys/class/tacho-motor/motor0/command
echo run-forever > /sys/class/tacho-motor/motor1/command
