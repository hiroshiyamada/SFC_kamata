#!/bin/bash
dir=Images
out=out
rm $dir/$out/*
for i in {1..14}
do
  cat $dir/*/$i.txt > $dir/$out/$i.txt
done
