from django.contrib import admin

from .models import News, Source

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    pass

@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    pass
