from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
from newspaper import Article
import re
import json
from datetime import datetime
import os
from pathlib import Path


######### Helper function  to fetch article details #########
def article_details(links, base_url, news_channel, category):
     
    result = []
    for e in links:
        
        try:
            res = requests.get(e)
            res.raise_for_status()
            
            article = Article(e)
            article.set_html(res.text)
            article.parse()
            # print("✅ Parsed:", e)
            # print("   Title:", article.title)
            
            data = {'Title':article.title,
                    'Authors': article.authors if article.authors else ['N/A'],
                    'Published': str(article.publish_date) if article.publish_date else 'N/A',
                    'News_channel':news_channel,
                    'category':category,
                    'url': e,
                    'Text': article.text
                    }

            
            result.append(data)
            
            
        except Exception as ex:
            print("⚠️ Skipped:", e, "because", ex)
    
    return result
    


Dict_of_news_sources = {
    
    'Abc' : {
            'sports':('https://www.abc.net.au/news/sport',r"/news/\d{4}-\d{2}-\d{2}/"),
            'finance':('https://www.abc.net.au/news/business/',r"/news/\d{4}-\d{2}-\d{2}/"),
            'lifestyle': ('https://www.abc.net.au/news/lifestyle/',r"/news/\d{4}-\d{2}-\d{2}/"),
            'Music': ('https://www.abc.net.au/news/music',r"/news/\d{4}-\d{2}-\d{2}/")
          },
     
    
    'SBS' : { 
            'sports':('https://www.sbs.com.au/sport', r"/sport/article/")
            
          },
    
    'Guardian' : {
                'sports': ('https://www.theguardian.com/au/sport',r"/\d{4}/[a-z]{3}/\d{2}/"),
                'lifestyle': ('https://www.theguardian.com/au/lifeandstyle',r"/\d{4}/[a-z]{3}/\d{2}/")
                }
                        }

All_articles_of_all_newsChannels = []

for news_channel, value in Dict_of_news_sources.items():
    for category, value_1 in value.items():
        # print(f"news_channel={news_channel}, category={category} ")
        
        # unpack the tuple
        base_url = value_1[0]
        regex_exp = value_1[1]
        
        # print(f"news_channel={news_channel}, category={category}, link = {regex_exp} ")
        
        result = requests.get(base_url)
        soup = BeautifulSoup(result.text,'html.parser')
        # print('hi there -----',result.text)
        # print()
        # print()
        
        
        # Loop through all anchor tags 'a' with href
        links = [link['href'] for link in soup.find_all("a", href=True) if re.search(regex_exp, link['href'])]
        # print(links[:5])

        # Join links (e.g. 'ABC' + 'news/world')
        links = [urljoin(base_url, link) for link in links]
        # print('news_channel ===',news_channel, links[:5])
        
        # for e in links:
        #     print(e)
        
        # print(len(links))
            
        # no duplicate
        links = list(dict.fromkeys(links))
        # print(len(links))
        
        # calling helper function to fetch article details
        meta_data = article_details(links, base_url, news_channel, category)
        
        #Combine all articles of all newschannels 
        All_articles_of_all_newsChannels.extend(meta_data)
        
print(len(All_articles_of_all_newsChannels))
print(json.dumps(All_articles_of_all_newsChannels, indent=2, ensure_ascii=False))


# Make a directory
RAW_DIR = Path('data/raw')
RAW_DIR.mkdir(parents=True, exist_ok=True)

filename = RAW_DIR / "news_raw.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(All_articles_of_all_newsChannels, f, indent=2, ensure_ascii=False)
    
print('Saved to =', filename)

    