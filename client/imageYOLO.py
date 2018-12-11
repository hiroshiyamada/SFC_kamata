import os
from operator import itemgetter
'''
入力データの形式 detection_results : [cat, score, bounds]
[(b'dog', 0.9993329048156738, (224.17959594726562, 378.47900390625, 178.75448608398438, 328.29620361328125)),
(b'bicycle', 0.991621732711792, (344.5289306640625, 286.759765625, 486.18890380859375, 321.3658447265625)), 
(b'truck', 0.9165929555892944, (580.9117431640625, 125.05439758300781, 208.13427734375, 87.27819061279297))]
'''

#楽譜の順番にソートする
def sortSheet(detection_results):
    #楽譜の順番にx座標でソートする
    detection_results = sorted(detection_results, key=lambda x: (x[2][1]), reverse=True)
    return detection_results

# 不要な認識結果を削除する(多重認識を消す、他の列の認識結果を消す)
def remove_duplicate(detection_results):
    #削除結果を格納するリスト
    removed_result = []
    for cat, score, bounds in detection_results:
        catstr = str(cat.decode("utf-8"))
        #x,y:認識結果の中心のx座標とy座標, w,h:バウンディングボックスの横と縦の長さ
       	x, y, w, h = bounds
       	#多重認識を消す(信頼度が60%を超えるかつx座標が400以上かつ800以下)
       	#if(score > 0.60 and x < 800 and x > 400):
        if(score > 0.60):
       	    removed_result.append((cat,score,bounds))
       	    #cv2.rectangle(img, (int(x - w / 2), int(y - h / 2)), (int(x + w / 2), int(y + h / 2)), (255, 0, 0), thickness=2)
            #cv2.putText(img,str(cat.decode("utf-8")),(int(x),int(y)),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,0))
    return removed_result
       	
       	
#チューリップ画像用リスト
dic_4cat = {"fa":("F4", "q"), "so":("G4", "q"), "la":("A4", "q"), "do":("C5", "q")}
#ジングルベル画像用リスト(2分音符あり)
dic_17jingle = {"u_do":("C4", "q"),"ul_do":("C4","h"),"u_re":("D4","q"),"ul_re":("D4","h"),\
"l_mi":("E4", "h"),"fa":("F4","q"),"l_fa":("F4","h"),"so":("G4","q"),"l_so":("G4","h"),\
"la":("A4", "q"),"l_la":("A4","h"),"si_F":("A#4/Bb4","q"),"h_do":("C5","q"),"hl_do":("C5","h"),\
"h_re": ("D5", "q"), "stop": ("Z", "q"), "l_stop": ("Z", "h")}
#ジングルベル画像用リスト(4分音符のみ)
dic_10jingle = {"u_do": ("C4", "q"), "u_re": ("D4", "q"), "mi": ("E4", "q"), "fa": ("F4", "q"), "so": ("G4", "q"),\
"la":("A4", "q"),"si_F":("A#4/Bb4","q"),"h_do":("C5","q"),"h_re": ("D5", "q"), "stop": ("Z", "q")}

# yolo認識結果の形式からplay_soundの形式に変換する
def convertNotes(detection_results, cat_note_dic):
    return [cat_note_dic[str(cat.decode("utf-8"))] for cat, score, bounds in detection_results]

# 新しく追加された音符を見つける
def findNewNotes(detected_notes, past_notes):
    if len(past_notes) == []:
        return detected_notes
    ## 検出された音符の最初と最後は誤認識が多いので使わない
    ## 検出された音符が少なすぎる場合は無視
    #if len(detected_notes) < 3:
    #    return []
    #detected_notes = detected_notes[1:-1]
    #if len(past_notes) < 3:
    #    return []
    #past_notes = past_notes[1:-1]
    best_i = 0
    best_eq_count = 0
    for i in  range(-3,len(past_notes)):
        eq_count = 0
        for j in range(len(detected_notes)):
            if i + j >= len(past_notes):
                break
            if i+ j < 0:
                continue
            if past_notes[i+j] == detected_notes[j]:
                eq_count += 1
        if eq_count >= best_eq_count:
            best_i = i
            best_eq_count = eq_count
    # 結果出力
    new_notes_begin = len(past_notes)-best_i -1
    print(new_notes_begin)
    if new_notes_begin >= len(detected_notes):
       return []
    return detected_notes[new_notes_begin+1:]
###### 古いコード
    # 過去ノートから認識結果ノートの先頭と同じノートを探す
    for i in range(len(past_notes)):
        #print("i",i)
        if (detected_notes[0] == past_notes[i]):
            # 認識結果ノートのが少なければ新しいノートなし
            # example : output_notes= [do, re , mi , fa]  detected_notes = [re, mi] i =1
            if len(past_notes) - i >= len(detected_notes):
                continue
            # 認識結果ノートが過去ノートと同じことを確認
            # example : output_notes = [do, re, mi, re, mi, fa]
            #           detected_notes =            [re, mi, fa, so, ra]
            #           i =1  j = 0, 1, 2, 3, 4
            for j in range(len(past_notes) - i):
                #print("j",j)
                if (detected_notes[j] != past_notes[i + j]):
                    break
            else:
                # 残りの認識結果ノートを出力
                return detected_notes[j+1:]
    return []

#yoloの入力結果から不要なものを削除しplay_soundの形式に変換する
def makeSound(detection_results):
    sortedInput = sortSheet(detection_results)
    removed_result = remove_duplicate(sortedInput)
    print("removedResults", removed_result)
    return convertNotes(removed_result, dic_10jingle)

if __name__ == "__main__":
    past =   [1,2,3]
    detected = [2,3,4,5]
    new = findNewNotes(detected, past)
    print("past ",past)
    print("detected ",detected)
    print("new ",new)
    
'''
    # net = Detector(bytes("cfg/densenet201.cfg", encoding="utf-8"), bytes("densenet201.weights", encoding="utf-8"), 0, bytes("cfg/imagenet1k.data",encoding="utf-8"))

    net = Detector(bytes("cfg/yolov3.cfg", encoding="utf-8"), bytes("weights/yolov3.weights", encoding="utf-8"), 0, bytes("cfg/coco.data",encoding="utf-8"))
    notes = []

    #img = cv2.imread(os.path.join(os.environ["DARKNET_HOME"],"data/dog.jpg"))
    img_transformed = cv2.imread("/home/sfc_kamata/work/SFC_kamata/darknet_update/cfg/tulip_many/img/1.jpg")


    # loop
    # img_transformed に変換後のopecv imageを入れる
    img_darknet = Image(img_transformed)
    results = net.detect(img_darknet)
    remove(results, notes)
    updateNotes(results, notes)

    for cat, score, bounds in results:
        x, y, w, h = bounds
        cv2.rectangle(img, (int(x - w / 2), int(y - h / 2)), (int(x + w / 2), int(y + h / 2)), (255, 0, 0), thickness=2)
        cv2.putText(img,str(cat.decode("utf-8")),(int(x),int(y)),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,0))

    cv2.imshow("output", img)
    # img2 = pydarknet.load_image(img)

    cv2.waitKey(0)
'''
