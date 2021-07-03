from .metrics import run_wordcloud
import base64
from io import BytesIO
import matplotlib.pyplot as plt
from .models import News, Source, Tweet
from django.shortcuts import render
from django.http import Http404
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# display matplotlib images in django without saving them locally
import matplotlib
matplotlib.use("Agg")


def home(request):
    sources = Source.objects.filter(active=1)
    return render(request, 'home.html', {'sources': sources, })


def author(request):
    return render(request, 'author.html')


def news_bysource(request, source_id):
    news_list = News.objects.filter(source=source_id).order_by('-updated_at')
    if news_list.count() == 0:
        raise Http404("Source not found")

    page = request.GET.get('page', 1)

    paginator = Paginator(news_list, 10)
    try:
        news = paginator.page(page)
    except PageNotAnInteger:
        news = paginator.page(1)
    except EmptyPage:
        news = paginator.page(paginator.num_pages)

    return render(request, 'news_by_source.html', {'source': news_list[0].source, 'news': news, })


def display_wordcloud(request):
    with open('media/wordcloud.png', 'rb') as f_image:
        image = f_image.read()

    return render(request, 'word_cloud.html', {'image': base64.b64encode(image).decode('utf-8')},)


def tweet_list(request):
    tweet_list = Tweet.objects.order_by('-published_date')
    if tweet_list.count() == 0:
        raise Http404("No tweets available")

    page = request.GET.get('page', 1)

    paginator = Paginator(tweet_list, 10)
    try:
        tweets = paginator.page(page)
    except PageNotAnInteger:
        tweets = paginator.page(1)
    except EmptyPage:
        tweets = paginator.page(paginator.num_pages)

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
    return render(request, 'search_results.html', {'results': search_results})
