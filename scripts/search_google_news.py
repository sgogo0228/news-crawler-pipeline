# 爬google news的新聞
import requests
from bs4 import BeautifulSoup

def show_progress(cur, total):
    ratio = cur/total
    print("\r", int(ratio*100), "% | ", "██"*int(20*ratio), "  "*(20-int(20*ratio)), " |", sep="", end="")

max_count = int(input("每間榮院新聞紀錄數量上限(預設為5筆)：") or "5")
# max_count = 5
path = r'C:\Users\sgogo\python_code\example\txt\google_news.txt'
key_list = ['北榮臺東', '北榮鳳林', '北榮玉里', '北榮蘇澳', '北榮員山', '高榮臺南', '中榮灣橋', '中榮埔里', '中榮嘉義', '屏榮龍泉', 
            '屏榮', '高榮', '北榮桃園', '北榮新竹', '臺中榮總', '臺北榮總']
key_num = len(key_list)
n = 0

with open(path, 'w', encoding='UTF-8') as f:
    for key in key_list:
        f.write('================' + key + '==============\n')

        # 爬此網址的新聞，其中"3d"是3天內的新聞
        res = requests.get("https://news.google.com/rss/search?q=" + key + "+when%3A3d&hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant")
        soup = BeautifulSoup(res.text, 'xml')
        news_group = soup.select('item')
        count = 1

        for item in news_group:
            f.write('-----[' + str(count) + ']-----\n')
            
            # 透過辨識xml標籤，取得新聞標題、網址、時間
            news_title = item.select_one('title').getText()
            news_url = item.select_one('link').getText()
            news_time = item.select_one('pubDate').getText()
            f.write(news_title + '\n')
            f.write(news_url + '\n')
            f.write(news_time + '\n')

            # 因為中榮北榮新聞比較多，紀錄特別多筆
            count += 1
            if count > 2*max_count: break
            if key != '臺中榮總' and key != '臺北榮總' and count > max_count: break
        f.write('\n\n')
        n += 1
        show_progress(n, key_num)