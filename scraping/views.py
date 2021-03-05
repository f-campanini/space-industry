from .models import News, Source
from django.shortcuts import render
from django.http import Http404

def home(request):
    news = News.objects.all()
    return render(request, 'home.html', { 'news':news, })

def news_bysource(request, source_id):
    news = News.objects.filter(source=source_id)
    if news.count() == 0:
        raise Http404("Source not found")
    return render(request, 'news_by_source.html', { 'source': news[0].source,
                                                    'news': news, }
                 )
