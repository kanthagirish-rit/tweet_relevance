
from django.http import HttpResponse
from django.template import loader

from core_algorithm import main

def index(request):
    return HttpResponse("Welcome to Tweet Relevance System!")
    #return HttpResponse(main())
    
    template = loader.get_template('tweetView/tweetView.html')

