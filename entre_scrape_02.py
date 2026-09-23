import requests
import bs4
import csv
import time
import re

# 1. output.csvの読み込み
with open('output.csv', encoding='utf-8_sig') as f:
    reader = csv.reader(f)
    header = next(reader)
    file1_list = list(reader)

print(f"output.csvの読み込み件数: {len(file1_list)}件")

# 2. エントレの上演情報をスクレイピング
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

url = 'https://entre-news.jp/theaterlist'
try:
    res = requests.get(url, headers=headers, timeout=10)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.content, 'html.parser')

    title_list = [t.getText().strip() for t in soup.select('.yyeTitle')]
    link_list = [l.get('href') for l in soup.select('.yyeDescription .bt_red') if l.get('href')]
    print(f"エントレから取得したタイトル数: {len(title_list)}件")

except Exception as e:
    print(f"エントレのスクレイピングでエラー: {e}")
    title_list = []
    link_list = []

def clean_title(text):
    if not text:
        return ""
    return re.sub(r'[『』【】（）()\s ]', '', text)

# 空文字を除外してクリーン化
clean_entre_titles = [clean_title(t) for t in title_list if clean_title(t)]

# 3. フィルタリング処理
filtered_list = []

for row in file1_list:
    if len(row) < 7:
        continue

    title = row[1]
    firstday = row[3]
    url_tag = row[5]
    official_url = row[6]

    if firstday == "＊＊＊＊＊":
        continue

    clean_tg_title = clean_title(title)
    
    # タイトル重複チェック（空文字を除外して厳密に判定）
    is_duplicate_title = False
    if clean_tg_title:
        for entre_t in clean_entre_titles:
            # 互いに2文字以上で部分一致するか確認
            if len(entre_t) >= 2 and (entre_t in clean_tg_title or clean_tg_title in entre_t):
                is_duplicate_title = True
                break

    if is_duplicate_title:
        continue

    # URL重複チェック
    is_duplicate_url = False
    for entre_link in link_list:
        if entre_link and len(entre_link) > 5:
            if entre_link in official_url or entre_link in url_tag:
                is_duplicate_url = True
                break

    if is_duplicate_url:
        continue

    filtered_list.append(row)

# 4. output_deleted.csv へ書き出し
with open('output_deleted.csv', 'w', newline='', encoding='utf-8_sig') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(filtered_list)

print(f"処理完了: {len(filtered_list)}件を残して保存しました。")
