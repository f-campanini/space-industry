# scraping
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import lxml
from celery import shared_task
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from .models import News

logger = get_task_logger(__name__)

# scraping function
#@shared_task(name="get_hacker_news")
@periodic_task(
    run_every=(crontab(minute='*/2')),
    name="task_hackernews_rss",
    ignore_result=True
)
def hackernews_rss():
    article_list = []
    try:
        print('Starting the scraping tool')
        # execute my request, parse the data using XML
        # parser in BS4
        r = requests.get('https://news.ycombinator.com/rss')
        soup = BeautifulSoup(r.content, features='xml')
        # select only the "items" I want from the data
        articles = soup.findAll('item')
    
        # for each "item" I want, parse it into a list
        for a in articles:
            title = a.find('title').text
            link = a.find('link').text
            published_wrong = a.find('pubDate').text
            published = datetime.strptime(published_wrong, '%a, %d %b %Y %H:%M:%S %z')            # print(published, published_wrong) # checking correct date format            # create an "article" object with the data
            # from each "item"
            article = {
                'title': title,
                'link': link,
                'published': published,
                'source': 'HackerNews RSS'
            }
            # append my "article_list" with each "article" object
            article_list.append(article)
            print('Finished scraping the articles')
    
            # after the loop, dump my saved objects into a .txt file
            return save_function(article_list)
    except Exception as e:
        print('The scraping job failed. See exception:')
        print(e)
        
@shared_task(serializer='json', name="task_save_news")
def save_function(article_list):
    print('starting task: Save articles')
    new_count = 0

    for article in article_list:
        try:
            News.objects.create(
                title = article['title'],
                link = article['link'],
                published = article['published'],
                source = article['source']
            )
            new_count += 1
        except Exception as e:
            print('failed at latest_article is none')
            print(e)
            break
    return print('finished')


