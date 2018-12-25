from pydarknet import Detector, Image
import cv2
import os

colorList = {'u_do': (0, 0, 255), 'u_re': (0, 255, 0), 'mi': (255,153,153), 'fa': (0, 255, 255), 'so': (255, 0, 255), \
'la': (255, 255, 0), 'si_F': (255,101,255), 'h_do': (114,152,0),'h_re': (255,255,153),'stop': (50,191,255)}

def yoloNetwork():
    net = Detector(bytes("/home/sfc_kamata/work/SFC_kamata/darknet_update/cfg/jingle/test.cfg", encoding="utf-8"), bytes("/home/sfc_kamata/work/SFC_kamata/darknet_update/cfg/jingle/backup/1208_1/yolo-obj_class4_20000.weights", encoding="utf-8"), 0, bytes("/home/sfc_kamata/work/SFC_kamata/darknet_update/cfg/jingle/jingle.data",encoding="utf-8"))
    return net

def yoloDetect_net(img, net):
    img2 = Image(img)
    results = net.detect(img2)
    return results

def yoloDetect(img):
    # net = Detector(bytes("cfg/densenet201.cfg", encoding="utf-8"), bytes("densenet201.weights", encoding="utf-8"), 0, bytes("cfg/imagenet1k.data",encoding="utf-8"))
    net = Detector(bytes("/home/sfc_kamata/work/SFC_kamata/darknet_update/cfg/jingle/test.cfg", encoding="utf-8"), bytes("/home/sfc_kamata/work/SFC_kamata/darknet_update/cfg/jingle/backup/1208_1/yolo-obj_class4_20000.weights", encoding="utf-8"), 0, bytes("/home/sfc_kamata/work/SFC_kamata/darknet_update/cfg/jingle/jingle.data",encoding="utf-8"))
    #img = cv2.imread(os.path.join(os.environ["DARKNET_HOME"],"data/dog.jpg"))
    #img = cv2.imread("/home/sfc_kamata/work/SFC_kamata/darknet_update/cfg/jingle/img/1.jpg")
    img2 = Image(img)
    # r = net.classify(img2)
    results = net.detect(img2)
    #writeBoundingBox(results)
    return results

def writeBoundingBox(results, img, num):
    print(results)
    for cat, score, bounds in results:
        print(cat)
        print(score)
        print(bounds)
       	x, y, w, h = bounds
        cv2.rectangle(img, (int(x - w / 2), int(y - h / 2)), (int(x + w / 2), int(y + h / 2)), colorList[cat.decode("utf-8")], thickness=2)
        cv2.rectangle(img, (int(x - w / 2), int(y - h / 2) - 30), (int(x - w / 2) + 70, int(y - h / 2)), colorList[cat.decode("utf-8")], thickness=-1)
        cv2.putText(img,str(cat.decode("utf-8")),(int(x - w / 2),int(y - h / 2)),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,0))
    #cv2.imshow("output", img)
    cv2.imwrite("output/output"+str(num).zfill(4)+".jpg", img)
    # img2 = pydarknet.load_image(img)
    #cv2.waitKey(0)

