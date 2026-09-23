
import requests
import bs4
import csv
import time
import re
import datetime


#output.csvを読み込む
file1 = open('output.csv', encoding='utf-8_sig')
file1_reader = csv.reader(file1)
file1_list = list(file1_reader)
print("全部で" + str(len(file1_list)-1) + "件")

#エントレ上演情報をスクレイピング
res = requests.get('https://entre-news.jp/theaterlist')
soup = bs4.BeautifulSoup(res.content, 'html.parser')
title_list = soup.select('.yyeTitle')
link_list = soup.select('.yyeDescription .bt_red')
print(link_list[0].get('href'))

#output.csvのタイトルを検索して、エントレにすでにあるタイトルだったらその行を空行にする
#output.csvの期間を検索して、＊＊＊＊＊だったらその行を空行にする
for k in range(len(title_list)):
    for i in range(len(file1_list)):
        if title_list[k].getText() in file1_list[i][1]:
            file1_list[i] = ['','','','','','','','','','','']
        if file1_list[i][3] == "＊＊＊＊＊":
            file1_list[i] = ['','','','','','','','','','','']
        if link_list[k].get('href') in file1_list[i][5]:
            file1_list[i] = ['','','','','','','','','','','']

file2_list = []
for n in range(len(file1_list)):
    if not file1_list[n] == ['','','','','','','','','','','']:
        file2_list.append(file1_list[n])


#重複削除したリストをoutput_deleted.csvに書き出し
output_file = open('output_deleted.csv', 'w', newline='', encoding='utf-8_sig')
output_writer = csv.writer(output_file)
output_writer.writerow(['post_id', 'post_type', 'post_status', 'post_title', '', 'post_content', 'post_category', 'firstday', 'lastday', 'short_title', 'theatre'])
for m in range(len(file2_list)):
    output_writer.writerow(file2_list[m])
output_file.close()

