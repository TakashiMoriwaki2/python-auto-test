
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



endTime = time.time() - startTime
endTime = str(int(endTime)) + '秒で出来ました！'
print(endTime)
