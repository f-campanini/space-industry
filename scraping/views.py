from .models import News
from .serializers import NewsSerializer
from rest_framework import generics

class NewsListCreate(generics.ListCreateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
