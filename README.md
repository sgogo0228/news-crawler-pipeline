# news-crawler-pipeline
Fetch news on FB and google for posts of the our pages

## Features

- 🔍 `search_fb_news.py`: Fetch recent posts from multiple Facebook pages and gather them into a single reviewable text file.
- 🌐 `search_google_news.py`: Pull recent news articles by keyword from Google News and save them as a text file.
- 📄 `scrap_one_news.py`: Given a confirmed news link, automatically extract the article title, content, and associated image.
- 📩 `msg2admin.py`: After the Facebook post is published, fetch the post URL and generate a formatted summary message for internal supervisors.

## Requirements
**Install required packages**

   ```bash
   pip install -r requirements.txt
  ```

## Usages

```
# Search Facebook pages for recent posts
python scripts/search_fb_news.py

# Search Google News by keywords
python scripts/search_google_news.py

# Extract content from a selected news article
python scripts/scrap_one_news.py

# Generate post-summary message for internal reporting
python scripts/msg2admin.py
```

- Each script is designed to run independently and save outputs as text files in your working directory. Some steps may require manual review or input.

## Project Structure
news-crawler-pipeline\
├── README.md\
├── requirements.txt\
├── scripts\
│   ├── search_fb_news.py\
│   ├── search_google_news.py\
│   ├── scrap_one_news.py\
│   └── msg2admin.py\
├── examples\
└── main.py


## Notes
- This project was developed to streamline the collection and dissemination of news content across internal and public channels.
- Each module is designed to be simple and replaceable based on actual workflow needs.
