#!/bin/bash
dir=/home/sfc_kamata/work/BBox-Label-Tool
out=out
rm $dir/$out/*

cd $dir/Images/increase/001
for f in *.jpg
do  
	list=$(echo $f | sed 's/\.[^\.]*$//')
	cat $dir/Images/increase/*/$list.txt > $dir/$out/$list.txt
done


#for i in {1..14}
#do
#  cat $dir/*/$i.txt > $dir/$out/$i.txt
#done
