import glob

classList = [0] * 10

for f in glob.glob("./img/*.txt"):
    # 行ごとにすべて読み込んでリストデータにする
    data = open(f, "r")
    lines = data.readlines()
    # 一行ずつ表示する
    for line in lines:
        classList[int(line[0])] = classList[int(line[0])] + 1
print(classList)
