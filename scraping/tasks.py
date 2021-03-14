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

@shared_task
def run_scraper():
    try:
        print('Starting the scraping tool')

        # retrieve an object for the sources
        # the object is a list and each item is a record in the database
        source_obj = Source.objects.all()
        
        for source_site in source_obj:
            if source_site.active:
                r = requests.get(source_site.link)
                soup = BeautifulSoup(r.content, features='xml')

                print('Start scraping source {} - id - {}'.format(source_site.name, source_site.id))

                articles = soup.findAll('item')
    
                for a in articles:
                    title = a.find('title').text
                    link = a.find('link').text
                    published_wrong = a.find('pubDate').text
                    published = datetime.strptime(published_wrong, '%a, %d %b %Y %H:%M:%S %z')
                    try:
                        News.objects.create(
                            title = title,
                            link = link,
                            published = published,
                            source = source_site
                        )
                    except Exception as e:
                        print(e)
                        continue

                print('Finished scraping source {}'.format(source_site.name))

        print('Finished scraping the articles')
    except Exception as e:
        print('The scraping job failed. See exception:')
        print(e)

