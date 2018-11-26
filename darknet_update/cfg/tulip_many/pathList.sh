#!/bin/bashs
rm_list=("15_" "16_" "17_" "18_" "19_" "20_" "21_" "22_" "23_" "24_");
dir=/home/sfc_kamata/work/SFC_kamata/darknet_update/cfg/tulip_many
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

for f in *.jpg
do
	fname=$(basename $f)
	fcomp=$(echo ${fname:0:3})
	if [[ ${rm_list[@]} != *$fcomp* ]]; then
    		echo $(realpath $f) >> $dir/tulip_many_images.txt
	fi
done
