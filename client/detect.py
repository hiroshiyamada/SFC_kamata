# -*- coding: utf-8 -*-

from pydarknet import Detector, Image
import cv2
import os

# 不要な認識結果を削除してノート化
def remove(detection_results, detected_notes):
    pass

# ノートを更新
def updateNotes(detected_notes, output_notes):
    # 出力ノートから認識結果ノートの先頭と同じノートを探す
    for i in range(len(output_notes)):
        if (detected_notes[0] == output_notes[i]):
            # 認識結果ノートのが少なければ終了(新しいノートなし)
            if len(output_notes) - i > len(detected_notes):
                return
            # 認識結果ノートが出力ノートと同じことを確認
            for j in range(len(output_notes) - i):
                if (detected_notes[j] != output_notes[i + j]):
                    break
            # 残りの認識結果ノートを出力ノートに追加
            output_notes.extend(detected_notes[j+1:])

if __name__ == "main":
    # init 
    net = Detector(bytes("cfg/yolov3.cfg", encoding="utf-8"), bytes("weights/yolov3.weights", encoding="utf-8"), 0, bytes("cfg/coco.data",encoding="utf-8"))
    notes = []

    # loop
    # img_transformed に変換後のopecv imageを入れる
    img_darknet = Image(img_transformed)
    results = net.detect(img_darknet)
    updateNotes(results, notes)

