from .models import News, Source, Tweet
from django.shortcuts import render
from django.http import Http404
from django.db.models import Q

# display matplotlib images in django without saving them locally
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from .metrics import run_wordcloud

def home(request):
    sources = Source.objects.filter(active=1)
    return render(request, 'home.html', {'sources':sources,})

def news_bysource(request, source_id):
    news = News.objects.filter(source=source_id).order_by('-updated_at')
    if news.count() == 0:
        raise Http404("Source not found")
    return render(request, 'news_by_source.html', {'source': news[0].source, 'news': news,})

def display_wordcloud(request):
    with open('media/wordcloud.png', 'rb') as f_image:
        image = f_image.read()

    return render(request, 'word_cloud.html', { 'image': base64.b64encode(image).decode('utf-8')},)

def tweet_list(request):
    """
    Allows editing the tweets to be published
    """
    tweets = Tweet.objects.order_by('-published_date')
    if tweets.count() == 0:
        raise Http404("Tweets not found")
    return render(request, 'tweet_list.html', {'tweets': tweets})

def index(request):
    '''
    The function is used by the search bar
    '''
    search_post = request.GET.get('search')
    if search_post:
        search_results = News.objects.filter(Q(title__icontains=search_post))
    else:
        search_results = News.objects.all()
    return render(request, 'search_results.html', { 'results': search_results })