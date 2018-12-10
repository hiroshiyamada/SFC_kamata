import cv2
import time
import os
import shutil

start = time.time()
target_dir = 'images'
shutil.rmtree(target_dir)
os.mkdir(target_dir)
cap = cv2.VideoCapture(0)
print('init %f' %(time.time() - start))
k = 0

while True :
    print('cap %f' %(time.time() - start))
    ret, frame = cap.read()
    frame = cv2.resize(frame , dsize=(800, 600))
    k_str = str(k).zfill(4)
    name = "images/" + k_str + ".jpg"
    cv2.imwrite(name, frame)
    k = k + 1
    cv2.waitKey(100)
    if (k > 3000):
        break
cap.release()
