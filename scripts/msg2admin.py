# 更新給長官訊息
# facebook_graphql_scraper.py、parser.py、utils.py都有修改，若內文有直接引用其他粉絲頁，fb回傳的json會包括內文和被引用的貼文，
# 且其中被引用的貼文會在封包更前面的位置，所以會抓到錯的時間，因此要傳入facebook_user_id去過濾
# (經過觀察json檔，data['story']['url']內的資料可以用來判斷是來自哪個粉絲頁)
if __name__ == "__main__":
    import sys, os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from setuptools import setup
from my_fb_graphql_scraper.facebook_graphql_scraper import FacebookGraphqlScraper as fb_graphql_scraper
from datetime import timedelta
import os

# days_limit = int(input('要抓過去幾天內的資料(預設為1天): ') or '1') # Number of days within which to scrape posts
# post_limit = int(input('要抓幾筆(預設為1筆): ') or '1')
days_limit = 1      # Number of days within which to scrape posts
post_limit = 2

facebook_user = ['vacweb1', '100067963924922']
path = r'C:\Users\sgogo\python_code\example\txt\msg2admin.txt'
driver_path = r"C:\Users\sgogo\python_code\chromedriver-win64\chromedriver-win64\chromedriver.exe" 
fb_spider = fb_graphql_scraper(driver_path=driver_path)

msg = '謝謝'
with open(path, 'r', encoding='UTF-8') as f:
    pre_str = f.read()
if pre_str != '':
    pre_str = pre_str[:-2] + '\n'

with open(path, 'w', encoding='UTF-8') as f:
    res1 = fb_spider.get_user_posts(fb_username_or_userid=facebook_user[0], days_limit=days_limit,display_progress=False)
    res2 = fb_spider.get_user_posts(fb_username_or_userid=facebook_user[1], days_limit=days_limit,display_progress=False)
    post_count = 0
    for one_post in res1['data']:
        if '#就醫保健處' in one_post['context']:
            one_post['published_date'] += timedelta(hours=8)
            title = one_post['context'].splitlines()[1]
            msg = '\n這是' + one_post['published_date'].strftime('%m%d %H%M') + '的FB貼文\n' + \
                 title + \
                '\n輔導會 https://www.facebook.com/vacweb1/posts/' + one_post['post_id'] + \
                '\n就醫處 https://www.facebook.com/100067963924922/posts/' + res2['data'][post_count]['post_id'] + '\n' + msg
            post_count += 1
        if post_count >= post_limit:
            break
    f.write(pre_str + msg[1:])
print("Finish")