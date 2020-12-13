import requests
import pandas as pd

print("データダウンロード開始")

# 自由に書き換える
# packId = "kp01" # 第1弾
packId = "kp02" # 第2弾
# packId = "cp01" # 第3弾（未実装。カードの順番が以前と変わったため、種類が特定できない）
# packId = "kp03" # 第4弾（未実装。カードの順番が以前と変わったため、種類が特定できない）
# packId = "max01" # 第5弾（未実装。カードの順番が以前と変わったため、種類が特定できない）
# ここまで

readCsv = '/Users/tsunodanaoki/work/Python/01_createCSV/output/'
outputImage = '/Users/tsunodanaoki/work/Python/02_downloanImages/picture/'

# CSV取得
df = pd.read_csv(readCsv + packId +'.csv', encoding="utf_8", dtype=object)

# データ表示
for rowNo in range(len(df)):
    url = df.iloc[rowNo]["URL"]
    file_name =  outputImage + packId + df.iloc[rowNo]["ID"] + ".jpg"

    response = requests.get(url)
    image = response.content

    with open(file_name, "wb") as aaa:
        aaa.write(image)

print("データダウンロード終了")
