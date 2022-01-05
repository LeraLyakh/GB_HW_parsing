from lxml import html
from pprint import pprint
import requests
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

client = MongoClient('localhost', 27017)
db = client['lenta_ru']
#////a[@class="card-mini _topnews"]|//a[@class="card-big _topnews _news"]


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'}
url = 'https://lenta.ru'
response = requests.get(url, headers=headers)
dom = html.fromstring(response.text)
main_news = dom.xpath('//a[@class="card-mini _topnews"]|//a[@class="card-big _topnews _news"]')

#print(len(main_news))
#scource = 'https://lenta.ru'
titles = dom.xpath('//a[@class="card-mini _topnews"]//span/text()|//a[@class="card-big _topnews _news"]//h3/text()')

links = dom.xpath('//a[@class="card-mini _topnews"]/@href|//a[@class="card-big _topnews _news"]/@href')
for i in range(len(links)):
    if links[i].startswith('https') is False:
        links[i]=url+links[i]

news_time = dom.xpath('//a[@class="card-mini _topnews"]//time/text()|//a[@class="card-big _topnews _news"]//time/text()')
#pprint(news_time)

#news_dict = {}
for i in range(len(titles)):
    news_dict = {}
    news_dict['_id'] = links[i].split('/')[2].split('.')[0]+news_time[i].split(':')[0]+news_time[i].split(':')[1]
    news_dict['name'] = titles[i]
    news_dict['link'] = links[i]
    news_dict['time'] = news_time[i]
    news_dict['source'] = links[i].split('/')[2]
    pprint(news_dict)
    try:
        db.lenta_news.insert_one(news_dict)
    except DuplicateKeyError:
        pass

#pprint(news_dict)
#pprint(db.lenta_news)
#print(db.lenta_news.count_documents({}))
