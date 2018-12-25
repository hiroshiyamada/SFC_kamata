#!/bin/bash
cd /home/sfc_kamata/work/SFC_kamata/darknet_update
#./darknet_tmp detector train cfg/jingle/jingle.data cfg/jingle/yolo-obj_class4.cfg 
./darknet_1000 detector train cfg/jingle/jingle.data cfg/jingle/yolo-obj_class4.cfg cfg/jingle/backup/yolo-obj_class4_20000.weights >> cfg/jingle/log_20000.txt

