import requests # ページリクエストのため
from bs4 import BeautifulSoup # スクレイピングのため
import re # 文字列操作のため
import pandas as pd # CSV操作のため

#### 関数定義（開始） ####

# 自由に書き換える
# packId = "kp01" # 第1弾
packId = "kp02" # 第2弾
# packId = "cp01" # 第3弾（未実装。カードの順番が以前と変わったため、種類が特定できない）
# packId = "kp03" # 第4弾（未実装。カードの順番が以前と変わったため、種類が特定できない）
# packId = "max01" # 第5弾（未実装。カードの順番が以前と変わったため、種類が特定できない）
# ここまで

urlTop = "https://www.konami.com/yugioh/rushduel/products/"
urlCenter = "cards/"
jpg = ".jpg"
sep = "/"
type = {"kp01" : (17,  20, 9, 5), "kp02" : (16, 20, 9, 6), "cp01" : (16, 20, 9, 6), "kp03" : (16, 20, 9, 6), "max01" : (16, 20, 9, 6)}

# エラー
ERROR = "99"

# レアリティ
RARITY_N = "00"
RARITY_R = "01"
RARITY_SR = "02"
RARITY_UR = "03"
RARITY_RR = "04"

# カー種別
TYPE_NM = "00"
TYPE_EM = "01"
TYPE_M = "02"
TYPE_T = "03"

# 出力
outputUrl = "/Users/tsunodanaoki/work/Python/01_createCSV/output/"
csv = ".csv"
#### 関数定義（終了） ####

#### 関数定義（開始） ####
def nullCheck(val):
    return val is None

# URL作成
def createUrl(filename):
    return urlTop + packId + sep + urlCenter + filename[filename.find("-") + 1:] + jpg

# レアリティを取得
def getRarity(filename):
    print(filename)
    # "-"で文字列を配列に変換（filenameの構成は「パックID-カードID-レアリティ」）
    list = filename.split("-")

    # レアリティが付与されていない場合は空となる
    if len(list) == 2:
        return RARITY_N

    # ３つ目の要素がレアリティ
    result = ERROR
    if list[2] == "r":
        result = RARITY_R
    elif list[2] == "sr":
        result = RARITY_SR
    elif list[2] == "ur":
        result = RARITY_UR
    elif list[2] == "rr":
        result = RARITY_RR

    return  result

# 種別を取得する
def getType(count, filename):
    if count <= type[packId][0]:
        return TYPE_NM
    elif count <= type[packId][0] + type[packId][1]:
        return TYPE_EM
    elif count <= type[packId][0] + type[packId][1] + type[packId][2]:
        return TYPE_M
    elif count <= type[packId][0] + type[packId][1] + type[packId][2] + type[packId][3]:
        return TYPE_T

    return ERROR

#### 関数定義（終了） ####


# スクレイピングの準備
# urlName = "https://www.konami.com/yugioh/rushduel/products/kp01/" # 第一弾
urlName = urlTop + packId
res = requests.get(urlName)
soup = BeautifulSoup(res.content, "html.parser")

# 結果
dogs = []
# 種別取得用のカウンター
count = 1

print("はじめ（辞書作成）")

# <li>の要素を取得
elems = soup.find_all("li")
print(elems)
# <li>の要素から必要な情報を抜き出す
for elem in elems:
    # <a>の要素を抜き出す
    a = elem.find('a')
    # 存在しない場合は処理をスキップ
    if nullCheck(a):
        continue;

    # name属性の値を取得
    name = a.get("name")

    # 存在しない場合は処理をスキップ
    if nullCheck(name):
        continue;

    # 「_」を「-」に変換
    name = name.replace("_", "-")
    # 結果をつめる
    dogs.append({"ID" : (str(count-1)).zfill(3), "URL" : createUrl(name), "NAME" : a.text, "TYPE" : getType(count, name), "RARITY" : getRarity(name)})
    # カード種別取得用のカウンターを更新（IDとしても使う）
    count = count + 1

print("辞書結果：", dogs)
print("終わり（辞書作成）")

print("はじめ（CSV作成）")
df = pd.json_normalize(dogs)
df.to_csv(outputUrl + packId + csv)
print("終わり（CSV作成）")
