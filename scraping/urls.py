from django.urls import path
from . import views

urlpatterns = [
    path('api/news/', views.NewsListCreate.as_view()),
]

