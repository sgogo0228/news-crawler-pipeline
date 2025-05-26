class element_path(object):
    GENERAL_TITLE_PATH = 'h1:not(:has(img))'
    # GENERAL_IMG_PATH = 'p:not([class]):not([style])~* img,' \
    #                     '*:has(~p:not([class]):not([style])) img,' \
    #                     '*:has(~* p:not([class]):not([style])) img,' \
    #                     'div[style*=background][style*=url]'

    GENERAL_IMG_PATH = 'div:has(p:not([class]):not([style])) img,' \
                    'div[style*=background][style*=url]'
    
    CONTENT_PATH = 'p:not([class], [style]), ' \
    'div.edit.news_edit, ' \
    'div.article-content-edtor, ' \
    'div.article_content'