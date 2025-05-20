from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from new_locator.locator import *
import requests
import re, time
from selenium.webdriver.support import expected_conditions as EC

# 刪除上次存的圖片
# for f in glob.glob("news_img*"):
#     os.remove(f)

driver_path = r".\chromedriver-win64\chromedriver-win64\chromedriver.exe"
svc = Service(driver_path)
driver = webdriver.Chrome(service=svc)
# url = "https://newstaiwan.net/2025/05/06/310893/" #台灣好報
# url = "https://ppt.cc/fVRprx" #東台先鋒報
# url = "https://udn.com/news/story/7327/8708684" #聯合報
# url = "https://tyenews.com/2025/05/840463/" #桃園電子報
# url = "https://www.cna.com.tw/news/ahel/202505060022.aspx" #中央社
# url = "https://news.ltn.com.tw/news/life/breakingnews/5034813" #自由時報 圖片必須被瀏覽到才會load
# url = "https://www.ettoday.net/amp/amp_news.php7?news_id=2956473&from=amp_newslist" #ETToday新聞雲
# url = "https://cnews.com.tw/204241003a02/" #匯流新聞網 
# url = "https://www.setn.com/News.aspx?NewsID=1653069" #三立新聞網
# url = "https://www.ctwant.com/article/415269/" #CTWANT
# url = "https://www.watchmedia01.com/archives/403886" #觀傳媒
# url = "https://www.cdns.com.tw/articles/1214936" #中華日報
# url = "https://youngnews3631.com/news_detail.php?NewsID=10368" #漾新聞
# url = "https://liff.line.me/1454987169-1WAXAP3K/v2/article/oqmX37w?utm_source=lineshare"    #line today 滾太快會抓不到圖片連結
# url = "https://old.ksnews.com.tw/w2025050850/" #更生新聞網 沒有標題在新聞頁面中、抓圖片會403，所以另開一個driver screenshot像素較差
# url = "https://act.chinatimes.com/market/content.aspx?AdID=18328&chdtv=" #中時
# url = "https://anntw.com/articles/20250216-7VE2" #台灣醒報
# url = "https://www.tristarnews.com.tw/news_ii.html?ID=30341" #三星傳媒 內文特規div.edit.news_edit
# url = "https://www.nownews.com/news/6680645" #NOWnews 抓圖片會403，所以另開一個driver screenshot像素較差 內文特規div.article-content-edtor
# url = "https://news.tvbs.com.tw/life/2864044" #TVBS 內文特規div.article_content
# url = "https://www.taiwantimes.com.tw/app-container/app-content/new/new-content-detail?blogId=blog-38caf962-5bb4-46d3-9bd8-39ba550cc216" #臺灣時報
# url = 'https://www.ydn.com.tw/news/newsInsidePage?chapterID=1764870' #青年日報 圖片特規 div[style*=background][style*=url]
# url = "https://tw.news.yahoo.com/%E5%8C%97%E6%A6%AE%E8%AD%B7%E7%90%86%E5%BE%B5%E6%89%8D%E5%8D%9A%E8%A6%BD%E6%9C%83-ai%E7%A7%91%E6%8A%80%E8%88%87%E9%A3%AF%E5%BA%97%E7%B4%9A%E5%AE%BF%E8%88%8D%E6%89%93%E9%80%A0%E5%8F%8B%E5%96%84%E8%81%B7%E5%A0%B4-%E7%8F%BE%E5%A0%B4%E8%BF%91%E7%99%BE%E4%BD%8D%E4%BA%BA%E5%93%A1%E5%85%B1%E8%A5%84%E7%9B%9B%E8%88%89-025952324.html" #奇摩新聞 網站內文高度特規 #Masterwrap
# url = input("請輸入網址：")

url = "https://pets.ettoday.net/news/2963625"

driver.get(url)
time.sleep(1)

# 有些網站必須圖片被瀏覽器刷到才會load
body_height = driver.find_element(By.TAG_NAME, 'body').rect["height"]
if 'tw.news.yahoo.com' in url:
    body_height = driver.find_element(By.ID, 'Masterwrap').rect["height"]
print(body_height)
# 這個1500跟瀏覽器的高度有關，滑到最底可能會刷到下個新聞的照片
for i in range(1, body_height-1000, 200):
    driver.execute_script(rf"window.scrollTo(0, {i})")
    time.sleep(0.02)

# #樣新聞、 更生新聞網沒有h1、臺灣醒報、#青年日報&#匯流新聞網加上:not(:has(img))才會跳到except
if 'youngnews' in url or 'old.ksnews' in url or 'anntw' in url or 'www.ydn.com' in url or 'cnews.com' in url:
    title = driver.title
else:
    title = driver.find_element(By.CSS_SELECTOR, element_path.GENERAL_TITLE_PATH).text
# title = driver.find_element(By.CSS_SELECTOR, ':has(h1):not(:has(img~h1, h1~img)) h1:not(:has(img))').text
    
# contents = driver.find_elements(By.CSS_SELECTOR, 'p:not([class]):not([style]), div.edit.news_edit, div.article-content-edtor, div.article_content')
contents = driver.find_elements(By.CSS_SELECTOR, element_path.CONTENT_PATH)
imgs = driver.find_elements(By.CSS_SELECTOR, element_path.GENERAL_IMG_PATH)

content_end_y = 0

msg = f"這是預計　發出的貼文\n#就醫保健處\n{title}\n\n"
for p in contents:
    if p.text:
        msg = msg + p.text + "\n\n"
        if p.rect["y"] > content_end_y:
            content_end_y = p.rect['y'] + p.rect['height']

msg = re.sub(r' ', '　', msg)
msg = re.sub(r'(?<!\d),|,(?<!\d)', '，', msg)
msg = re.sub(r';', '；', msg)
msg = re.sub(r'(?<!\d)-|-(?<!\d)', '－', msg)
msg = re.sub(r'(?<!\d)\.|\.(?<!\d)', '。', msg)
msg = re.sub(r'(?<!\d):|:(?<!\d)', '：', msg)

msg = msg + url
with open(rf".\example\txt\one_news.txt", 'w', encoding='utf-8') as f:
    f.write(msg)

title = re.sub('[^\u4E00-\u9FFF]', '', title)
n = 1
for img in imgs:
    if r"https://www.ydn.com.tw" in url:
        src = img.get_attribute('style')
        src = re.sub(r".+(https:\/\/www\.ydn\.com\.tw.+\.jpg).+", "\\1", src)
    else:
        src = img.get_attribute('src')
    # download the image
    if img.rect['width']>100 and img.rect['height']>100:
        if img.rect["y"] > content_end_y:
            if img.rect["y"] - content_end_y < 150:
                content_end_y = img.rect["y"] + img.rect["height"]
            else: break
        if src and "svg" not in src:
            src = re.sub('jpg.+', 'jpg', src)
            src = re.sub('webp.+', 'webp', src)
            r = requests.get(src, allow_redirects=True)

            # nownews、更生新聞網用requests會被拒絕存取，因此再開一個driver直接用screenshot，解析度較差
            if r.status_code == 403:
                driver2 = webdriver.Chrome(service=svc)
                driver2.get(src)
                img = driver2.find_element(By.TAG_NAME, "img")
                img.screenshot(rf".\img\{n}_{title}img.jpg")
                driver2.quit()
            else:
                open(rf".\example\img\{n}_{title}img.jpg", 'wb').write(r.content)

            n += 1
test = input("any")
driver.quit()
