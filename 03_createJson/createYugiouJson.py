import pandas as pd
import json
import collections as cl
from collections import namedtuple

print("遊戯王カードのJSONを作成する")

# 自由に書き換える
packId = "kp01" # 第1弾
# packId = "kp02" # 第2弾
# packId = "cp01" # 第3弾（未実装。カードの順番が以前と変わったため、種類が特定できない）
# packId = "kp03" # 第4弾（未実装。カードの順番が以前と変わったため、種類が特定できない）
# packId = "max01" # 第5弾（未実装。カードの順番が以前と変わったため、種類が特定できない）
# ここまで

# CSV取得
df = pd.read_csv('/Users/tsunodanaoki/work/Python/01_createCSV/output/' + packId + '.csv', encoding="utf_8", dtype=object)

# 配列　→　JSON
# list = []
list = []
# 配列作成
for rowNo in range(len(df)):
    dic = cl.OrderedDict()
    dic["no"] = rowNo
    dic["id"] = df.iloc[rowNo]["ID"]
    dic["url"] = "http://localhost:8080/static/card/kp01/" + "kp01" + dic["id"] + ".jpg"
    dic["name"] = df.iloc[rowNo]["NAME"]
    dic["type"] = df.iloc[rowNo]["TYPE"]
    dic["rarity"] = df.iloc[rowNo]["RARITY"]
    dic["pack"] = "kp01"
    list.append(dic)


# JSON作成
result = json.dumps(list, ensure_ascii=False)

# ファイル書き出し
with open("/Users/tsunodanaoki/work/Python/03_createJson/output/cardListJSon" + packId + ".json", "w") as f:
    f.write(result)

print("結果")
print(result)
