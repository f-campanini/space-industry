# word cloud script
import numpy as np
import pandas as pd
# from PIL import image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt

# to import dataset from django queryset
from django_pandas.io import read_frame

import requests
from datetime import datetime
from celery import shared_task
from celery.task.schedules import crontab
from celery.utils.log import get_task_logger
from .models import News, Source

logger = get_task_logger(__name__)

def run_wordcloud():
    # retrieve the entire dataset from the News table
    # possible improvement would be to pass a timerange through the endpoing
    # and use it to create the plot
    news_queryset = News.objects.all()
    
    # now build the pandas datasets using only the column title from the queryset
    df = read_frame(news_queryset, fieldnames=['title'])

    text = " ".join(title for title in df.title)

    # lower max_font_size, change the maximum number of word and lighten the background:
    wordcloud = WordCloud(max_font_size=50, background_color="white").generate(text)
    # when changing the figure size check which is the dpi set in the views
    plt.figure(figsize=(3, 2))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")

    # return the plot
    return plt
