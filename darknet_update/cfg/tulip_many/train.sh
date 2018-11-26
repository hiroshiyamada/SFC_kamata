#!/bin/bash
cd /home/sfc_kamata/work/SFC_kamata/darknet_update
./darknet detector train cfg/tulip_many/tulip_many.data cfg/tulip_many/yolo-obj_class4.cfg
