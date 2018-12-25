#!/bin/bash

echo "Content-type: text/html"
echo ""
read line
set ${line}
r=${1}
l=${2}
sound=${*:3}
#echo $r
#echo $l
#echo $sound
echo $r > /sys/class/tacho-motor/motor0/speed_sp
echo $l > /sys/class/tacho-motor/motor1/speed_sp
echo run-forever > /sys/class/tacho-motor/motor0/command
echo run-forever > /sys/class/tacho-motor/motor1/command
echo $sound > test.fifo
