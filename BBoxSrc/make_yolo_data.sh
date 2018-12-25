#!/bin/bash

cls_num=10
yolo_dir=/home/sfc_kamata/work/SFC_kamata/darknet_update/cfg/jingle/img

#中間ファイルを削除
rm Images/increase/*/* -f
rm training_images/*/* -f
rm $yolo_dir/* -f
rm out/* -f

for i in {001..010}; do
  echo $i
  cp Images/$i/* Images/increase/$i;
  cp Labels/$i/* training_images/$i;
done

#スクリプトを順に実行
python increase_picture.py ${cls_num}
#python3 gray.py ${cls_num}
python3 convert.py ${cls_num}
bash cat_yamada.sh
cp out/* $yolo_dir 
cp Images/increase/001/*.jpg $yolo_dir 
cd /home/sfc_kamata/work/SFC_kamata/darknet_update/cfg/jingle/
rm jingle_images.txt
bash pathList.sh
