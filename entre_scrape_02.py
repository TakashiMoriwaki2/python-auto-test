import requests
import bs4
import csv
import time
import re

# --------------------------------------------------
# 1. output.csvの読み込み（ヘッダーとデータを分離）
# --------------------------------------------------
with open('output.csv', encoding='utf-8_sig') as f:
    reader = csv.reader(f)
    header = next(reader)       # 1行目（ヘッダー）を取り出す
    file1_list = list(reader)  # 2行目以降のデータのみ取得

print(f"output.csvの読み込み件数: {len(file1_list)}件")

# --------------------------------------------------
# 2. エントレの上演情報をスクレイピング（User-Agent指定）
# --------------------------------------------------
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

url = 'https://entre-news.jp/theaterlist'
try:
    res = requests.get(url, headers=headers, timeout=10)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.content, 'html.parser')

    # タイトルとリンクを取得
    title_list = [t.getText().strip() for t in soup.select('.yyeTitle')]
    link_elements = soup.select('.yyeDescription .bt_red')
    link_list = [l.get('href') for l in link_elements if l.get('href')]

    print(f"エントレから取得したタイトル数: {len(title_list)}件")

except Exception as e:
    print(f"エントレのスクレイピングでエラーが発生しました: {e}")
    title_list = []
    link_list = []

# タイトルの記号やスペースを除去して比較しやすくする関数
def clean_title(text):
    if not text:
        return ""
    return re.sub(r'[『』【】（）()\s ]', '', text)

clean_entre_titles = [clean_title(t) for t in title_list]

# --------------------------------------------------
# 3. 重複・不要行のフィルタリング処理
# --------------------------------------------------
filtered_list = []

for row in file1_list:
    if len(row) < 7:
        continue  # データが不完全な行はスキップ

    title = row[1]        # タイトル
    firstday = row[3]     # 開始日
    url_tag = row[5]      # URLタグ
    official_url = row[6] # URL

    # 条件A: 日付が "＊＊＊＊＊" の場合は除外
    if firstday == "＊＊＊＊＊":
        continue

    # 条件B: エントレに既に存在するタイトルかチェック
    clean_tg_title = clean_title(title)
    is_duplicate_title = False
    for entre_t in clean_entre_titles:
        if entre_t and (entre_t in clean_tg_title or clean_tg_title in entre_t):
            is_duplicate_title = True
            break

    if is_duplicate_title:
        continue

    # 条件C: 公式URLが一致しているかチェック
    is_duplicate_url = False
    for entre_link in link_list:
        if entre_link and (entre_link in official_url or entre_link in url_tag):
            is_duplicate_url = True
            break

    if is_duplicate_url:
        continue

    # すべてのチェックを通過した行のみ残す
    filtered_list.append(row)

# --------------------------------------------------
# 4. output_deleted.csv へ書き出し（7列構造を維持）
# --------------------------------------------------
with open('output_deleted.csv', 'w', newline='', encoding='utf-8_sig') as f:
    writer = csv.writer(f)
    writer.writerow(header)       # 元と同じヘッダー（7列）を出力
    writer.writerows(filtered_list) # フィルタリング後のデータを出力

print(f"処理完了: {len(filtered_list)}件のデータを output_deleted.csv に保存しました。")
