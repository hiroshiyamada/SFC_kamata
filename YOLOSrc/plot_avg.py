#!/usr/bin/python2

import sys
import matplotlib.pyplot as plt

with open("iou.txt") as f:
  out = [map(float,l.rstrip().split(" ")) for l in f]
  
for o in out:
  iou =   sum(o[:12])/12
  index = o[12]
  loss =  o[13]
  print("index",index,"loss",loss,"iou",iou)

iou =   [sum(o[:12])/12 for o in out]
index = [o[12]  for o in out]
loss =  [o[13]  for o in out]
plt.plot(index, loss,index, iou)
plt.show()
