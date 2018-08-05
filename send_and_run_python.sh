#!/bin/sh

scp $1 robot@49.135.4.15:/home/robot/
ssh robot@49.135.4.15 python3 $1
