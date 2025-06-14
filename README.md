# News Crawler Pipeline｜新聞爬蟲自動整理系統

News Crawler Pipeline is a modular Python-based automation system that collects content from Facebook pages and Google News. It is designed to support social media content planning and internal reporting by streamlining the process of gathering, extracting, and formatting news-related information.\
本系統為一套模組化的 Python 自動化工具，協助從 Facebook 粉專與 Google News 擷取新聞資訊，整合為貼文規劃與主管彙報使用，減少人工搜尋與資料整理的工作量。

---
## 🔧 Features｜功能模組

- `scripts/search_fb_news.py`  
  Fetch recent posts from multiple Facebook pages and gather them into a single reviewable text file.  
  擷取多個 Facebook 粉專貼文，整合為一份可人工篩選的文字檔。

- `scripts/search_google_news.py`  
  Pull recent news articles by keyword from Google News and save them as a text file.  
  依關鍵字從 Google News 擷取近期新聞並儲存為文字檔。

- `scripts/scrap_one_news.py`  
  Given a confirmed news link, automatically extract the article title, content, and associated image.  
  對人工確認的新聞連結，自動擷取標題、內文與圖片。

- `scripts/msg2admin.py`  
  After the Facebook post is published, fetch the post URL and generate a formatted summary message for internal supervisors.  
  貼文發佈後，自動擷取連結並生成格式化彙報訊息。

---
## 🧩 Custom `fb_graphql_scraper` Module (`my_fb_graphql_scraper`)

### Why 為什麼需要自製版本：

1. Facebook 載入新文章時，會重複擷取上次最後一篇文章  
   When loading new posts by scrolling, the original module would repeatedly fetch the last post from the previous batch.
2. 若文章內引用其他貼文，時間會抓成被引用貼文的時間，導致判斷錯誤  
   If a post contains a shared reference, only the referenced post’s timestamp is fetched, causing time misalignment.

### What was changed 修改內容：

1. `requests_flow()` method in `FacebookGraphqlScraper`  
   → `before_time` 變數將記錄上次擷取的最後一則貼文時間，避免重複載入  
2. `find_creation()` method in `utils/utils.py`  
   → 調整判斷邏輯，排除被引用貼文時間的誤判

### Location 模組位置：

- Module: `my_fb_graphql_scraper`
- Used in: `scripts/search_fb_news.py`、`scripts/msg2admin.py`

---
## 📦 Requirements｜安裝需求

```bash
pip install -r requirements.txt
```

---
## 🚀 Usages｜使用方式

```bash
# 擷取 Facebook 粉專貼文
python scripts/search_fb_news.py

# 擷取 Google 新聞文章
python scripts/search_google_news.py

# 擷取選定新聞之標題、內容與圖片
python scripts/scrap_one_news.py

# 生成 Facebook 貼文連結的彙報訊息
python scripts/msg2admin.py
```

- Each script runs independently and saves output as text files. Manual review may be required between steps.\
  每個模組皆可獨立執行，並自動儲存輸出檔案；部分步驟需人工確認。

---
## 🧪 Example Outputs｜範例輸出

- `examples/txt/fb_output.txt`: 粉絲頁貼文彙整範例（由 `search_fb_news.py` 產生）
- `examples/txt/google_output.txt`: Google 新聞搜尋輸出（由 `search_google_news.py` 產生）
- `examples/txt/scraped_news.txt`: 擷取新聞標題與內文（`scrap_one_news.py` 產生）
- `examples/txt/admin_msg.txt`: 自動化格式回報（`msg2admin.py` 產生）
- `examples/img/`: 擷取的新聞配圖範例（`scrap_one_news.py` 產生）

---
## 📁 Project Structure｜專案結構
```python
news-crawler-pipeline/
├── chromedriver-win64
│ └── chromedriver-win64
│   └── chromedriver.exe # The position of chrome driver (version 137)
├── example/ # 範例輸出資料
│ ├── img/ # 儲存圖片截圖
│ └── txt/ # 儲存文字輸出（fb_news.txt, google_news.txt, 等）
├── my_fb_graphql_scraper/ # customed module 修改版FB爬蟲模組
├── scripts/ # 主執行腳本
│ ├── msg2admin.py
│ ├── scrap_one_news.py
│ ├── search_fb_news.py
│ └── search_google_news.py
├── util/ # 公用模組
│ └── locator.py # selector 定位器
├── requirements.txt # 套件安裝清單
└── README.md
```

---
## 🖥️ Executable files generation | 產生執行檔
This porject is developed aimed to be used in Windows environment without python and VS code. The executable files can be generated by following steps:  
- Install pyinstaller package ```bash bash pip install pyinstaller```
- Generate executable file ```bash pyinstaller -F scripts/search_fb_news.py```
- Copy `search_google_news.exe`, `/my_fb_graphql_scraper`, `/example` and driver to a directory (e.g. /exe) for executing independently. The structure of directory should be like this:  
```
exe  
├── search_google_news.exe  
├── example  
├── my_fb_graphql_scraper  
└── chromedriver-win64
```
My exe directory isn't on the repo due to the file size. You can DM me for getting my exe via LinkedIn:  
https://www.linkedin.com/in/da-ming-huang/

### Trouble shooting
- The problem in this site may happen when running the executable files on another system:  
https://github.com/wkeeling/selenium-wire/issues/402  
It seems to be pypassed by packing ca.crt and ca.key into the executable files:  
`pyinstaller -F --add-data="ca.crt;seleniumwire" --add-data="ca.key;seleniumwire" scripts/search_fb_news.py`
The files can run successfully for crawling posts on Facebook despite a error pops up (I haven't resolved it).

---
## 📎 Notes｜備註
- This project uses Selenium for web scraping. You need to install the appropriate browser driver based on your browser version. If you're using Google Chrome, download the matching version of ChromeDriver (https://sites.google.com/chromium.org/driver/). The driver (`chromedriver-win64/chromedriver-win64/chromedriver.exe`) in this repo corresponds to the developed environmont, win64 and Chrome version 137. You may replace it as needed.  
本專案使用 Selenium 進行爬蟲，需下載對應的瀏覽器driver。如果使用 Chrome，請下載對應版本的 ChromeDriver。本repo內之driver (`chromedriver-win64/chromedriver-win64/chromedriver.exe`)對應win64、Chrome version 137的開發環境，請視需求進行替換。  

- By default, scraped results (text and screenshots) are saved in 'example/txt/' and 'example/img/', and you can modify these paths in the scripts as needed.  
預設輸出路徑為 example/txt/ 和 example/img/，請依照需要修改腳本中的儲存路徑。

- This project was developed to streamline the collection and dissemination of news content across internal and public channels.\
本專案旨在簡化社群與內部新聞彙整流程，減少人工處理與資訊遺漏。

- Each module is designed to be simple and replaceable based on actual workflow needs.\
所有模組皆具獨立性，可依實務需求自由替換或調整。
