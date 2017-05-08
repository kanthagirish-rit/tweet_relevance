from django.shortcuts import render
from .models import getTrends, getTweets
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json


@csrf_exempt
def index(request):
    """
    :param request: HttpRequest
    :return: renders the home page of the application
    """
    return render(request, 'tweets/start.html')


@csrf_exempt
def home(request):
    """
    :param request: HttpRequest
    :return: trends as json response
    """
    print("views.home()")
    woeid = int(request.POST['woeid'])
    category = request.POST['category']
    data = getTrends(woeid, category)
    for item in data:
        item["trend"] = item["_id"]
        del item["_id"]
    d = {"woeid": woeid, "data": data}
    print("sending response")

    return HttpResponse(json.dumps(d), content_type='application/json')


@csrf_exempt
def tweets(request):
    """
    :param request: HttpRequest
    :return: tweets under the selected trend as json response
    """
    print("views.tweets()")
    trend = request.POST['trend']
    woeid = int(request.POST['woeid'])
    data = getTweets(trend, woeid)
    print("sending json response")
    return HttpResponse(json.dumps(data), content_type='application/json')
