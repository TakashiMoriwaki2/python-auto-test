
import requests
import bs4
import csv
import time
import re
from datetime import datetime
import os

startTime = time.time()

output_file = open('output.csv', 'w', newline='', encoding='utf-8_sig')
output_writer = csv.writer(output_file)

output_writer.writerow(['post_id', 'post_title', 'theaterName','firstday', 'lastday','URLtag', 'URL'])


#シアタークリエ
res = requests.get('https://crea.tohostage.com/lineup/index.html')
res.raise_for_status()
soup = bs4.BeautifulSoup(res.content, 'html.parser')
title_list = soup.select('.lineup_content h3')
kikan_list = soup.select('.date')
link_list = soup.select('.poster a')

for i in range(len(title_list)):
    title = title_list[i].getText()
    link = link_list[i].get('href')
    linkTag = '<a href="' + link + '" rel="noopener" class="q_button rounded bt_red sz_s">オフィシャルサイト</a>'
    if '～' in kikan_list[i].getText():
        first = kikan_list[i].getText().split('～')[0]
        last = kikan_list[i].getText().split('～')[1]
    else:
        first = '＊＊＊＊＊'
        last = '＊＊＊＊＊'
    shortTitle = title_list[i].getText()
    output_writer.writerow(['', title, 'シアタークリエ', first, last, linkTag , link])

output_file.close()
print('スクレイピング完了')
print('output.csvに保存完了')


"""
指定された日付が現在よりも過去かどうかを判定する関数
"""

def is_past_date(date_str):

    try:
        # 開始日を解析（"2025年1月25日（土）" → "2025年1月25日"）
        start_date = date_str.split("（")[0].strip()
        date_obj = datetime.strptime(start_date, "%Y年%m月%d日")
        
        # 現在の日付と比較
        return date_obj < datetime.now()
    except ValueError:
        return False  # エラー時は削除しない

"""
4列目の日付範囲をチェックし、過去の日付の行を削除して上書き保存
"""
def clean_csv(input_csv):

    output_data = []

    # CSVファイルを読み込み
    with open(input_csv, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file)
        header = next(reader)  # ヘッダーを保持

        for row in reader:
            if len(row) >= 4 and not is_past_date(row[3]):  # 4列目が過去なら削除
                output_data.append(row)

    # 上書き保存
    with open(input_csv, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(header)  # ヘッダーを書き込み
        writer.writerows(output_data)  # フィルタリングしたデータを書き込み

# 実行（ファイル名を適宜変更してください）
csv_filename = "output.csv"
clean_csv(csv_filename)
print("処理が完了しました。")

import pandas as pd


"""
B列のタイトルが重複している行を削除
"""
# 対象のCSVファイル名
csv_filename = "output.csv"  # ← ファイル名を適宜変更

# CSVを読み込む
df = pd.read_csv(csv_filename)

# B列（インデックス1）で重複を削除（先頭だけ残す）
df_deduplicated = df.drop_duplicates(subset=df.columns[1], keep="first")

# 元のCSVファイルに上書き保存（encoding="utf-8-sig" を追加）
df_deduplicated.to_csv(csv_filename, index=False, encoding="utf-8-sig")

print("✅ B列の重複を削除してCSVファイルに上書き保存しました。")



# エントレの上演情報をスクレイピングして比較
import entre_scrape_02

print('output_deleted.csvに保存完了')

# 日付を整理
import date_seiri



endTime = time.time() - startTime
endTime = str(int(endTime)) + '秒で出来ました！'
print(endTime)
