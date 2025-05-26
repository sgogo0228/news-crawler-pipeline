# 爬FB的新聞
if __name__ == "__main__":
    import sys, os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from setuptools import setup
from my_fb_graphql_scraper.facebook_graphql_scraper import FacebookGraphqlScraper as fb_graphql_scraper

def show_progress(cur, total):
    ratio = cur/total
    print("\r", int(ratio*100), "% | ", "██"*int(20*ratio), "  "*(20-int(20*ratio)), " |", sep="", end="")

days_limit = int(input('要抓過去幾天內的資料(預設為1天): ') or '1') # Number of days within which to scrape posts
# day_limit = 1

facebook_user_list = [['北榮臺東', '100063930725320'], 
                      ['北榮鳳林', '100057305747373'], 
                      ['北榮玉里', 'vhylfans'], 
                      ['北榮蘇澳', 'sabtpevgh'], 
                      ['北榮員山', 'ysbtpevgh'], 
                      ['高榮臺南', 'vghyk063125101'], 
                      ['中榮灣橋', '100057104546927'], 
                      ['中榮埔里', 'pulivh'], 
                      ['中榮嘉義', 'vhcy052359630'], 
                      ['屏榮', 'ptvgh'], 
                      ['高榮', 'vghks'], 
                      ['北榮桃園', 'vghtpe.tyvh'], 
                      ['北榮新竹', 'VHCT01'], 
                      ['臺中榮總', 'vghtc'], 
                      ['臺北榮總', 'vghtpe']]
user_num = len(facebook_user_list)
n = 0

path = r'C:\Users\sgogo\python_code\example\txt\fb_news.txt'
driver_path = r"C:\Users\sgogo\python_code\chromedriver-win64\chromedriver-win64\chromedriver.exe" 
fb_spider = fb_graphql_scraper(driver_path=driver_path)

with open(path, 'w', encoding='UTF-8') as f:
    for facebook_user in facebook_user_list:
        facebook_user_name = facebook_user[1]
        res = fb_spider.get_user_posts(fb_username_or_userid=facebook_user_name, days_limit=days_limit,display_progress=True)

        f.write('===========' + facebook_user[0] + '===============\n')
        for one_post in res['data']:

            # 若該貼文友內文(有可能只是轉連結)，最多紀錄200字，以利篩選
            if one_post['context']:
                f.write('-------------------\n')
                if len(one_post['context']) < 200:
                    f.write(one_post['context'] + '\n')
                else:
                    f.write(one_post['context'][:200] + '\n')
                f.write(one_post['post_url'] + '\n')
        f.write('\n')
        n += 1
        show_progress(n, user_num)
print("Finish")