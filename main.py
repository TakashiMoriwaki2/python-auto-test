
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

#日生劇場
res = requests.get('https://www.nissaytheatre.or.jp/schedule/')
res.raise_for_status()
soup = bs4.BeautifulSoup(res.content, 'html.parser')
title_list = soup.select('p.tit.min')
kikan_list = soup.select('.opendate')
link_list = soup.select('.btn-gold a')
link_list2 = []
for i in range(len(link_list)):
    if "詳細はこちら" in link_list[i].getText():
        link_list2.append(link_list[i])

for i in range(len(kikan_list)):
    title = title_list[i].getText()
    link = link_list2[i].get('href')
    first = kikan_list[i].getText().replace("・","～")
    linkTag = '<a href="' + link + '" rel="noopener" class="q_button rounded bt_red sz_s">オフィシャルサイト</a>'
    shortTitle = title_list[i].getText()
    output_writer.writerow(['', title, '日生劇場', first, "", linkTag , link])



#新橋演舞場
res = requests.get('https://www.shochiku.co.jp/play/schedules/?theater=enbujyo')
res.raise_for_status()
soup = bs4.BeautifulSoup(res.text, 'html.parser')
title_list = soup.select('.info .description')
kikan_list = soup.select('.time')
link_list = soup.select('.info a')
link_list2 = []

for j in range(len(link_list)):
    if j%2 == 0:
        link_list2.append(link_list[j])

for i in range(len(title_list)):
    title = title_list[i].getText()
    link = link_list2[i].get('href')
    linkTag = '<a href="' + link + '" rel="noopener" class="q_button rounded bt_red sz_s">オフィシャルサイト</a>'
    first = kikan_list[i].getText()
    last = ""
    shortTitle = title_list[i].getText()
    output_writer.writerow(['', title, '新橋演舞場', first, last, linkTag , link])

#PARCO劇場
res = requests.get('https://stage.parco.jp/calendar/')
res.raise_for_status()
soup = bs4.BeautifulSoup(res.text, 'html.parser')
title_list = soup.select('.mainCont__scheduleList__item__txt--ttl')
kikan_list = soup.select('.mainCont__scheduleList__item__txt--date')
link_list = soup.select('.box-in a')
link_list2 = []
for i in range(len(link_list)):
    if i%2 != 0:
        link_list2.append(link_list[i])

for i in range(len(title_list)):
    title = title_list[i].getText().strip()
    first = kikan_list[i].getText()
    link = '<a href="https://stage.parco.jp' + link_list2[i].get('href') + '" rel="noopener" class="q_button rounded bt_red sz_s">オフィシャルサイト</a>'
    #末尾の数字とスラッシュを削除して作品ページのリンクにする
    link2 = re.sub(r'\d+/$', '', link)
    output_writer.writerow(['', title, 'PARCO劇場', first, '' ,link2, ''])



#東京建物ブリリアホール
res = requests.get('https://toshima-theatre.jp/event/')
res.raise_for_status()
soup = bs4.BeautifulSoup(res.text, 'html.parser')
title_list = soup.select('h3')
kikan_list = soup.select('.date')
link_list = soup.select('h3 a')

for i in range(len(title_list)):
    title = title_list[i].getText().strip().replace("\n", "")
    link = "https://toshima-theatre.jp" + link_list[i].get('href')
    linkTag = '<a href="' + link + '" rel="noopener" class="q_button rounded bt_red sz_s">オフィシャルサイト</a>'
    if '～' in kikan_list[i].getText():
        first = kikan_list[i].getText().split('～')[0]
        last = kikan_list[i].getText().split('～')[1]
    else:
        first = '＊＊＊＊＊'
        last = '＊＊＊＊＊'
    shortTitle = title_list[i].getText()
    output_writer.writerow(['', title, '東京建物ブリリアホール', first, last, linkTag , link])

#MILANO-Za
res = requests.get('https://milano-za.jp/events/')
res.raise_for_status()
soup = bs4.BeautifulSoup(res.content, 'html.parser')
title_list = soup.select('.event-block .text-block h3')
kikan_list =soup.select('.event-block .schedule')
link_list = soup.select('.events-list .event-block a')

for i in range(len(title_list)):
    title = title_list[i].getText().strip().replace("\n", "")
    link = "https://milano-za.jp/events/" + link_list[i].get('href')
    linkTag = '<a href="' + link + '" rel="noopener" class="q_button rounded bt_red sz_s">オフィシャルサイト</a>'
    if '～' in kikan_list[i].getText():
        first = kikan_list[i].getText().split('～')[0]
        last = kikan_list[i].getText().split('～')[1]
    else:
        first = '＊＊＊＊＊'
        last = '＊＊＊＊＊'
    shortTitle = title_list[i].getText()
    output_writer.writerow(['', title, 'MILANO-Za', first, last, linkTag , link])

#新国立劇場
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options # ←追加

# --- GitHubの画面なしサーバーで動かすための設定 ---
options = Options()
options.add_argument('--headless')
driver = webdriver.Firefox(options=options) # optionsを指定して起動
# --------------------------------------------------

url = 'https://www.nntt.jac.go.jp/performance/'
driver.get(url)
time.sleep(3)  #3秒待つ
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
title_list = soup.select('.pf_BoxListLead')
kikan_list = soup.select('.pf_BoxListDays')
link_list = soup.select('.pf_BoxListLink')

for i in range(len(title_list)):
    title = title_list[i].getText().strip().replace("\n", "")
    link = "https://www.nntt.jac.go.jp" + str(link_list[i].get('href'))
    linkTag = '<a href="' + link + '" rel="noopener" class="q_button rounded bt_red sz_s">オフィシャルサイト</a>'
    if '～' in kikan_list[i].getText():
        first = kikan_list[i].getText().split('～')[0]
        last = kikan_list[i].getText().split('～')[1]
    else:
        first = '＊＊＊＊＊'
        last = '＊＊＊＊＊'
    shortTitle = title_list[i].getText()
    output_writer.writerow(['', title, '新国立劇場', first, last, linkTag , link])

driver.quit()




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


# ==========================================
# B列のタイトルが重複している行を削除 ＆ 除外リストで弾く
# ==========================================
csv_filename = "output.csv"  # ← ファイル名を適宜変更

# CSVを読み込む
df = pd.read_csv(csv_filename)

# 1. B列（インデックス1）で重複を削除（先頭だけ残す）
df = df.drop_duplicates(subset=df.columns[1], keep="first")

# 2. 除外リストを読み込んでフィルターをかける
exclude_file = 'exclude_list.txt'
if os.path.exists(exclude_file):
    with open(exclude_file, 'r', encoding='utf-8') as f:
        # 空行を省いてリスト化
        exclude_words = [line.strip() for line in f if line.strip()]
    
    print("以下のキーワードを含む公演を除外します:", exclude_words)
    
    # 'post_title' 列に除外キーワードが含まれていない行だけを残す
    for word in exclude_words:
        df = df[~df['post_title'].str.contains(word, na=False, case=False)]
else:
    print(f"除外リスト({exclude_file})が見つかりません。除外処理をスキップします。")

# 元のCSVファイルに上書き保存（encoding="utf-8-sig" を追加）
df.to_csv(csv_filename, index=False, encoding="utf-8-sig")

print("✅ B列の重複削除と除外リストの適用が完了し、上書き保存しました。")



# エントレの上演情報をスクレイピングして比較
import entre_scrape_02

print('output_deleted.csvに保存完了')

# 日付を整理
import date_seiri



endTime = time.time() - startTime
endTime = str(int(endTime)) + '秒で出来ました！'
print(endTime)
