# coding: UTF-8
import cv2
import matplotlib.pyplot as plt
import numpy as np

'''
############
関数名: fit
内容:   最良の拡大縮小率とマッチングされた場所(インデックス)を返す関数。
        複数のテンプレート画像(templates)をそれぞれ拡大縮小しながら、
        元画像(img)とテンプレートマッチングさせ、類似度が閾値(threshold)を
        超えた個数が最大になった時点を、最良の拡大縮小率とする。

入力:   img: 二値化した画像
        templates: グレイスケールで読み込んだテンプレート画像を格納したリスト
        start_percent: テンプレート画像拡大縮小率の最小値(%)
        stop_percent: テンプレート画像拡大縮小率の最大値(%)
        threshold: テンプレートマッチングの類似度の閾値(0〜1.0)
        
出力:   best_locations: 最良の拡大縮小率の際にテンプレート画像とマッチングしたインデックス
        best_scale: 最良のテンプレート画像の拡大縮小率
############ 
'''
def fit(img, templates, start_percent, stop_percent, threshold):
    img_width, img_height = img.shape[::-1]
    #閾値を超えたインデックスの個数の最大値を保持する変数
    best_location_count = -1
    #最良インデックスを格納する変数
    best_locations = []
    #最良の拡大縮小率を格納する変数
    best_scale = 1
    #cloud9では不要
    ##########
    plt.axis([0, 2, 0, 1])
    plt.show(block=False)

    x = []
    y = []
    ##########
    #3%刻みで拡大縮小率を変更して順番にscaleに入れる
    for scale in [i/100.0 for i in range(start_percent, stop_percent + 1, 3)]:
        #入力画像について、各テンプレート画像の類似度が閾値を超えたインデックスを格納する変数
        locations = []
        #入力画像について、各テンプレート画像との類似度が閾値を超えた個数をカウントする変数
        location_count = 0
        #テンプレート画像を順番に取り出す
        for template in templates:
            #テンプレート画像を縦横それぞれscale倍に拡大
            template = cv2.resize(template, None,
                fx = scale, fy = scale, interpolation = cv2.INTER_CUBIC)
            #テンプレートマッチングして、類似度を表すグレースケール画像にする
            #入力画像(img)のサイズが (W x H) ，テンプレート画像(template)のサイズが (w x h) の時，
            #出力画像のサイズ(result)は (W-w+1, H-h+1) になる
            result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
            #result画像(２次元配列)について、類似度が閾値以上の部分のインデックス取り出す
            result = np.where(result >= threshold)
            #result画像のうち閾値を超えたインデックスの個数を足し合わせる
            location_count += len(result[0])
            #インデックスを格納する(locationsは3次元配列になる)
            locations += [result]
        print("scale: {0}, hits: {1}".format(scale, location_count))
        #拡大縮小率と閾値を超えたインデックスの個数でグラフを書く。cloud9では描画されない。
        #########
        x.append(location_count)
        y.append(scale)
        plt.plot(y, x)
        plt.pause(0.00001)
        #########
        #閾値を超えたインデックスの個数が最大のものをbest_変数に格納する
        if (location_count > best_location_count):
            best_location_count = location_count
            best_locations = locations
            best_scale = scale
            plt.axis([0, 2, 0, best_location_count])
        elif (location_count < best_location_count):
            pass
    plt.close()
    #最良の拡大縮小率(best_scale)とその際のインデックス(best_locations)を返す
    return best_locations, best_scale