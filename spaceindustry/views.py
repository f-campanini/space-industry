from django.shortcuts import render
from django.views import generic

# Create your views here.
class HomePageView(generic.ListView):
    template_name = 'home.html'