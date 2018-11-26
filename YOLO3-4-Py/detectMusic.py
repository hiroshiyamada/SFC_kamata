from pydarknet import Detector, Image
import cv2
import os

def yoloDetect(img):
    # net = Detector(bytes("cfg/densenet201.cfg", encoding="utf-8"), bytes("densenet201.weights", encoding="utf-8"), 0, bytes("cfg/imagenet1k.data",encoding="utf-8"))

    net = Detector(bytes("/home/sfc_kamata/work/SFC_kamata/darknet_update/cfg/tulip_many/test.cfg", encoding="utf-8"), bytes("/home/sfc_kamata/work/SFC_kamata/darknet_update/cfg/tulip_many/backup/yolo-obj_class4_final.weights", encoding="utf-8"), 0, bytes("/home/sfc_kamata/work/SFC_kamata/darknet_update/cfg/tulip_many/tulip_many.data",encoding="utf-8"))

    #img = cv2.imread(os.path.join(os.environ["DARKNET_HOME"],"data/dog.jpg"))
    #img = cv2.imread("/home/sfc_kamata/work/SFC_kamata/darknet_update/cfg/tulip_many/img/1.jpg")
    img2 = Image(img)

    # r = net.classify(img2)
    results = net.detect(img2)
    #バウンディングボックスを描画する
    #writeBoundingBox(results)
    return results

def writeBoundingBox(results, img):
    print(results)
    for cat, score, bounds in results:
        print(cat)
        print(score)
        print(bounds)
       	x, y, w, h = bounds
        cv2.rectangle(img, (int(x - w / 2), int(y - h / 2)), (int(x + w / 2), int(y + h / 2)), (255, 0, 0), thickness=2)
        cv2.putText(img,str(cat.decode("utf-8")),(int(x),int(y)),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,0))
    #cv2.imshow("output", img)
    cv2.imwrite("output.jpg", img)
    # img2 = pydarknet.load_image(img)
    #cv2.waitKey(0)

