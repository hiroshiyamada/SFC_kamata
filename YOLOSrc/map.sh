#!/bin/bash
cd /home/sfc_kamata/work/SFC_kamata/darknet_update
#./darknet_tmp detector train cfg/jingle/jingle.data cfg/jingle/yolo-obj_class4.cfg 
./darknet detector train cfg/jingle/jingle.data cfg/jingle/yolo-obj_class4.cfg cfg/jingle/backup/yolo-obj_class4_49000.weights >> cfg/jingle/log_49000.txt

