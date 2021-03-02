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
from .models import News, Source

logger = get_task_logger(__name__)

# scraping function
@periodic_task(
    run_every=(crontab(minute='*/2')),
    name="task_hackernews_rss",
    ignore_result=True
)
def hackernews_rss():
    article_list = []
    try:
        print('Starting the scraping tool')

        r = requests.get('https://news.ycombinator.com/rss')
        soup = BeautifulSoup(r.content, features='xml')

        articles = soup.findAll('item')
    
        for a in articles:
            title = a.find('title').text
            link = a.find('link').text
            published_wrong = a.find('pubDate').text
            published = datetime.strptime(published_wrong, '%a, %d %b %Y %H:%M:%S %z')
            article = {
                'title': title,
                'link': link,
                'published': published,
                'source': 'HackerNews RSS'
            }

            article_list.append(article)
            try:
                source_obj = Source.objects.all()
                News.objects.create(
                    title = article['title'],
                    link = article['link'],
                    published = article['published'],
                    source = Source.objects.all()[0]
                )
            except Exception as e:
                print(e)
                continue
                        
        print('Finished scraping the articles')
    except Exception as e:
        print('The scraping job failed. See exception:')
        print(e)

