# coding: UTF-8
import sys
import subprocess
import cv2
import time
import numpy as np
from best_fit import fit
from rectangle import Rectangle
from note import Note
from random import randint
from midiutil.MidiFile3 import MIDIFile

#五線譜部分のテンプレートファイルパス(staff*.png)
staff_files = [
    "resources/template/staff2.png", 
    "resources/template/staff.png"]
quarter_files = [
    "resources/template/quarter.png", 
    "resources/template/solid-note.png"]
sharp_files = [
    "resources/template/sharp.png"]
flat_files = [
    "resources/template/flat-line.png", 
    "resources/template/flat-space.png" ]
half_files = [
    "resources/template/half-space.png", 
    "resources/template/half-note-line.png",
    "resources/template/half-line.png", 
    "resources/template/half-note-space.png"]
whole_files = [
    "resources/template/whole-space.png", 
    "resources/template/whole-note-line.png",
    "resources/template/whole-line.png", 
    "resources/template/whole-note-space.png"]

#グレイスケールで各種テンプレート画像を読み込み、配列として格納
staff_imgs = [cv2.imread(staff_file, 0) for staff_file in staff_files]
quarter_imgs = [cv2.imread(quarter_file, 0) for quarter_file in quarter_files]
sharp_imgs = [cv2.imread(sharp_files, 0) for sharp_files in sharp_files]
flat_imgs = [cv2.imread(flat_file, 0) for flat_file in flat_files]
half_imgs = [cv2.imread(half_file, 0) for half_file in half_files]
whole_imgs = [cv2.imread(whole_file, 0) for whole_file in whole_files]

startPercent = 50
endPercent = 150

staff_lower, staff_upper, staff_thresh = startPercent, endPercent, 0.77
sharp_lower, sharp_upper, sharp_thresh = startPercent, endPercent, 0.70
flat_lower, flat_upper, flat_thresh = startPercent, endPercent, 0.77
quarter_lower, quarter_upper, quarter_thresh = startPercent, endPercent, 0.70
half_lower, half_upper, half_thresh = startPercent, endPercent, 0.70
whole_lower, whole_upper, whole_thresh = startPercent, endPercent, 0.70

'''
############
関数名: locate_images
内容:   テンプレート画像とマッチングした長方形部分をRectangleクラスのインスタンスで返す
入力:   img: 二値化した画
        templates: グレイスケールで読み込んだテンプレート画像を格納したリスト
        start: テンプレート画像拡大縮小率の最小値(%)
        stop: テンプレート画像拡大縮小率の最大値(%)
        threshold: テンプレートマッチングの類似度の閾値(0〜1.0)
出力:   img_locations: テンプレート画像とマッチングした長方形部分のRectangleクラスのインスタンス
                       2リスト
############
'''
def locate_images(img, templates, start, stop, threshold):
    #最もよくマッチングした際の、テンプレート画像の拡大縮小率(scale)と、
    #テンプレート画像がマッチングした場所(locations)を算出
    locations, scale = fit(img, templates, start, stop, threshold)
    img_locations = []
    for i in range(len(templates)):
        w, h = templates[i].shape[::-1]
        #テンプレート画像を拡大縮小
        w *= scale
        h *= scale
        #マッチングした場所をRectangleクラスのインスタンスにする
        img_locations.append([Rectangle(pt[0], pt[1], w, h) for pt in zip(*locations[i][::-1])])
    return img_locations

'''
############
関数名: merge_recs
内容: 重なっているrecをまとめる
入力 recs: Rectangleのリスト
     threshold: 重なっているとする面積の割合のしきい値
出力 処理結果のRectangleのリスト
############
'''
def merge_recs(recs, threshold):
    filtered_recs = []
    while len(recs) > 0:
        #recsから順番にrecをrに取り出す
        r = recs.pop(0)
        #rからの距離でソート
        recs.sort(key=lambda rec: rec.distance(r))
        merged = True
        #rとの結合が終わるまでループ
        while(merged):
            merged = False
            i = 0
            #recsの残りを順番にrと比較
            for _ in range(len(recs)):
                #重なっている面積がどちらかのrecの面積のthreshold以上の割合ならrecsを結合
                if r.overlap(recs[i]) > threshold or recs[i].overlap(r) > threshold:
                    r = r.merge(recs.pop(i))
                    merged = True
                #rからの距離が横幅の合計の半分より大きくなったらループ終了する
                #（真横にずれている場合絶対重ならないから？）
                elif recs[i].distance(r) > r.w/2 + recs[i].w/2:
                    break
                else:
                    i += 1
        #結合したrを出力リストに追加
        filtered_recs.append(r)
    return filtered_recs

def open_file(path):
    pass
    #cmd = {'linux2':'eog', 'win32':'explorer', 'darwin':'open'}[sys.platform]
    #subprocess.run([cmd, path])

if __name__ == "__main__":
    #画像ファイルの指定
    img_file = sys.argv[1:][0]
    #画像の読み込み
    img = cv2.imread(img_file, 0)
    #グレイスケールに変換
    img_gray = img#cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.cvtColor(img_gray,cv2.COLOR_GRAY2RGB)
    #二値化処理
    #ret,img_gray = cv2.threshold(img_gray,127,255,cv2.THRESH_BINARY)
    ret,img_gray = cv2.threshold(img_gray,0, 255, cv2.THRESH_OTSU)
    img_width, img_height = img_gray.shape[::-1]
    #二値化した画像を出力
    cv2.imwrite('blachWhite_127.png', img_gray)
    #exit();

    #空白部分の位置を算出する
    print("Matching staff image...")
    staff_recs = locate_images(img_gray, staff_imgs, staff_lower, staff_upper, staff_thresh)

    #小さいバウンディングボックスの削除
    print("Filtering weak staff matches...")
    #staff_recsの内包配列を展開
    staff_recs = [j for i in staff_recs for j in i]
    #1次配列。staff_recsの2列目要素+最後に0を追加(avgの平均を下げるため)
    heights = [r.y for r in staff_recs] + [0]
    #1次配列。heightsの値でヒストグラムを作成
    histo = [heights.count(i) for i in range(0, max(heights) + 1)]
    #スカラー値。histoの平均を算出
    avg = np.mean(list(set(histo)))
    #avgより高いy値を持つstaff_recsだけを残す
    staff_recs = [r for r in staff_recs if histo[r.y] > avg]

    print("Merging staff image results...")
    staff_recs = merge_recs(staff_recs, 0.01)
    #入力画像をコピー
    staff_recs_img = img.copy()
    #入力画像のコピーに空白認識結果を重ねて描画
    for r in staff_recs:
        r.draw(staff_recs_img, (0, 0, 255), 2)
    #空白認識結果画像をファイル出力
    cv2.imwrite('staff_recs_img.png', staff_recs_img)
    open_file('staff_recs_img.png')

    print("Discovering staff locations...")
    #楽譜の行を囲うstaff_boxesを作成
    #（横幅を画像サイズと同じにしたstaff_recsの重なっているものを結合）
    staff_boxes = merge_recs([Rectangle(0, r.y, img_width, r.h) for r in staff_recs], 0.01)
    #処理結果を描画しファイル出力
    staff_boxes_img = img.copy()
    for r in staff_boxes:
        r.draw(staff_boxes_img, (0, 0, 255), 2)
    cv2.imwrite('staff_boxes_img.png', staff_boxes_img)
    open_file('staff_boxes_img.png')
    
    print("Matching sharp image...")
    sharp_recs = locate_images(img_gray, sharp_imgs, sharp_lower, sharp_upper, sharp_thresh)

    print("Merging sharp image results...")
    sharp_recs = merge_recs([j for i in sharp_recs for j in i], 0.5)
    sharp_recs_img = img.copy()
    for r in sharp_recs:
        r.draw(sharp_recs_img, (0, 0, 255), 2)
    cv2.imwrite('sharp_recs_img.png', sharp_recs_img)
    open_file('sharp_recs_img.png')

    print("Matching flat image...")
    flat_recs = locate_images(img_gray, flat_imgs, flat_lower, flat_upper, flat_thresh)

    print("Merging flat image results...")
    flat_recs = merge_recs([j for i in flat_recs for j in i], 0.5)
    flat_recs_img = img.copy()
    for r in flat_recs:
        r.draw(flat_recs_img, (0, 0, 255), 2)
    cv2.imwrite('flat_recs_img.png', flat_recs_img)
    open_file('flat_recs_img.png')

    print("Matching quarter image...")
    quarter_recs = locate_images(img_gray, quarter_imgs, quarter_lower, quarter_upper, quarter_thresh)

    print("Merging quarter image results...")
    quarter_recs = merge_recs([j for i in quarter_recs for j in i], 0.5)
    quarter_recs_img = img.copy()
    for r in quarter_recs:
        r.draw(quarter_recs_img, (0, 0, 255), 2)
    cv2.imwrite('quarter_recs_img.png', quarter_recs_img)
    open_file('quarter_recs_img.png')

    print("Matching half image...")
    half_recs = locate_images(img_gray, half_imgs, half_lower, half_upper, half_thresh)

    print("Merging half image results...")
    half_recs = merge_recs([j for i in half_recs for j in i], 0.5)
    half_recs_img = img.copy()
    for r in half_recs:
        r.draw(half_recs_img, (0, 0, 255), 2)
    cv2.imwrite('half_recs_img.png', half_recs_img)
    open_file('half_recs_img.png')

    print("Matching whole image...")
    whole_recs = locate_images(img_gray, whole_imgs, whole_lower, whole_upper, whole_thresh)

    print("Merging whole image results...")
    whole_recs = merge_recs([j for i in whole_recs for j in i], 0.5)
    whole_recs_img = img.copy()
    for r in whole_recs:
        r.draw(whole_recs_img, (0, 0, 255), 2)
    cv2.imwrite('whole_recs_img.png', whole_recs_img)
    open_file('whole_recs_img.png')

    note_groups = []
    #楽譜の行ごとに
    for box in staff_boxes:
        #縦位置が行の中心から一定以内の四角を取り出しNoteにする
        staff_sharps = [Note(r, "sharp", box) 
            for r in sharp_recs if abs(r.middle[1] - box.middle[1]) < box.h*5.0/8.0]
        staff_flats = [Note(r, "flat", box) 
            for r in flat_recs if abs(r.middle[1] - box.middle[1]) < box.h*5.0/8.0]
        quarter_notes = [Note(r, "4,8", box, staff_sharps, staff_flats) 
            for r in quarter_recs if abs(r.middle[1] - box.middle[1]) < box.h*5.0/8.0]
        half_notes = [Note(r, "2", box, staff_sharps, staff_flats) 
            for r in half_recs if abs(r.middle[1] - box.middle[1]) < box.h*5.0/8.0]
        whole_notes = [Note(r, "1", box, staff_sharps, staff_flats) 
            for r in whole_recs if abs(r.middle[1] - box.middle[1]) < box.h*5.0/8.0]
        staff_notes = quarter_notes + half_notes + whole_notes
        staff_notes.sort(key=lambda n: n.rec.x)
        staffs = [r for r in staff_recs if r.overlap(box) > 0]
        staffs.sort(key=lambda r: r.x)
        note_color = (randint(0, 255), randint(0, 255), randint(0, 255))
        note_group = []
        i = 0; j = 0;
        while(i < len(staff_notes)):
            if (staff_notes[i].rec.x > staffs[j].x and j < len(staffs)):
                r = staffs[j]
                j += 1;
                if len(note_group) > 0:
                    note_groups.append(note_group)
                    note_group = []
                note_color = (randint(0, 255), randint(0, 255), randint(0, 255))
            else:
                note_group.append(staff_notes[i])
                staff_notes[i].rec.draw(img, note_color, 2)
                i += 1
        note_groups.append(note_group)

    for r in staff_boxes:
        r.draw(img, (0, 0, 255), 2)
    #res.png    
        r.draw(img, (0, 0, 255), 2)
    flat_recs_img = img.copy()
    for r in flat_recs:
        r.draw(img, (0, 0, 255), 2)
        
    cv2.imwrite('res.png', img)
    open_file('res.png')
   
    for note_group in note_groups:
        print([ note.note + " " + note.sym for note in note_group])

    midi = MIDIFile(1)
     
    track = 0   
    time = 0
    channel = 0
    volume = 100
    
    midi.addTrackName(track, time, "Track")
    midi.addTempo(track, time, 140)
    
    for note_group in note_groups:
        duration = None
        for note in note_group:
            note_type = note.sym
            if note_type == "1":
                duration = 4
            elif note_type == "2":
                duration = 2
            elif note_type == "4,8":
                duration = 1 if len(note_group) == 1 else 0.5
            pitch = note.pitch
            midi.addNote(track,channel,pitch,time,duration,volume)
            time += duration

    midi.addNote(track,channel,pitch,time,4,0)
    # And write it to disk.
    binfile = open("output.mid", 'wb')
    midi.writeFile(binfile)
    binfile.close()
    open_file('output.mid')
