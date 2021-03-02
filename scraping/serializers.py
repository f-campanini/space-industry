from rest_framework import serializers
from .models import Source, News

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ('id', 'title', 'link', 'published', 'created_at', 'source')
