#!/bin/bash
cd /home/sfc_kamata/work/SFC_kamata/darknet_update
./darknet detector test cfg/tulip_many/tulip_many.data cfg/tulip_many/test.cfg cfg/tulip_many/backup/yolo-obj_class4_final.weights cfg/tulip_many/img/$1.jpg
