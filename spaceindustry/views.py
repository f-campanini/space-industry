from django.shortcuts import render
from django.views import generic
from scraping.models import News 

# Create your views here.
class HomePageView(generic.ListView):
    template_name = 'home.html'
    context_object_name = 'articles' 
    # assign "News" object list to the object "articles"
    
    # pass news objects as queryset for listview
    def get_queryset(self):
        print("publishing results")
        news_object = News.objects.all()
        return news_object
        
    def output_table(request):
        output = News()
        return render('home.html', {'output': output})

def handler404(request, *args, **argv):
    response = render_to_response('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response