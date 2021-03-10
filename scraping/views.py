from .models import News, Source
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
    news = News.objects.all()
    sources = Source.objects.all()
    return render(request, 'home.html', {'news':news, 'sources':sources,})

def news_bysource(request, source_id):
    news = News.objects.filter(source=source_id)
    if news.count() == 0:
        raise Http404("Source not found")
    return render(request, 'news_by_source.html', {'source': news[0].source, 'news': news,})

def display_wordcloud(request):
    plt = run_wordcloud()
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=200)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')
    buf.close()
    return render(request, 'word_cloud.html', { 'image': image_base64},)

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