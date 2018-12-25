#!/bin/bashs
#rm_list=("15_" "16_" "17_" "18_" "19_" "20_" "21_" "22_" "23_" "24_");
rm_list=("xxx");
rm_increase_list="5 7 8 9 10 11 12 13 14 15 16 17"
dir=/home/sfc_kamata/work/SFC_kamata/darknet_update/cfg/jingle
cd $dir/img

#getting real path 
realpath ()
{
    f=$@;
    if [ -d "$f" ]; then
        base="";
        dir="$f";
    else
        base="/$(basename "$f")";
        dir=$(dirname "$f");
    fi;
    dir=$(cd "$dir" && /bin/pwd);
    echo "$dir$base"
}

for i in $rm_increase_list
do
	rm -f $dir/img/*_$i.*
done

for f in *.jpg
do
	fname=$(basename $f)
	fcomp=$(echo ${fname:0:3})
	if [[ ${rm_list[@]} != *$fcomp* ]]; then
    		echo $(realpath $f) >> $dir/jingle_images.txt
	fi
done
