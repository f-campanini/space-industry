from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from scraping import views

urlpatterns = [
    path('', views.home , name='home'), # homepage
    path('sources/<int:source_id>/', views.news_bysource, name="news_by_source"),
    path('admin/', admin.site.urls),
    path('metrics/word_cloud/', views.display_wordcloud, name="word_cloud"),
    path('search/', views.index, name="index"),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
