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
    '''
    Parses all the sources, check for new articles and the article to the database
    '''
    try:
        print('Starting the scraping tool')

        source_obj = Source.objects.all()
        
        for source_site in source_obj:
            if source_site.active:
                r = requests.get(source_site.link)
                soup = BeautifulSoup(r.content, features='xml')

                print('Start scraping source {} - id - {}'.format(source_site.link, source_site.id))

                articles = soup.findAll('item')
    
                for a in articles:
                    title = a.find('title').text
                    link = a.find('link').text

                    # check if the article is already in the database
                    # if it is in the DB, skip the article
                    # an improvement will be to compare the timestamp
                    try:
                        if News.objects.get(link=link):
                            continue
                    except News.DoesNotExist:
                        print("New article found {}".format(link))

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

