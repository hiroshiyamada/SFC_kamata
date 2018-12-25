#!/bin/bash
cd /home/sfc_kamata/work/SFC_kamata/darknet_update
./darknet detector test cfg/jingle/jingle.data cfg/jingle/test.cfg cfg/jingle/backup/yolo-obj_class4_final.weights cfg/jingle/img/$1.jpg
