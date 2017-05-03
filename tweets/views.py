from django.shortcuts import render, HttpResponse
from .models import getTrends, getTweets
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json


@csrf_exempt
def index(request):
    return render(request, 'tweets/start.html')


@csrf_exempt
def home(request):
    """
    :param request:
    :return:
    """
    print("views.home()")
    woeid = None
    if request.method == 'POST':
        woeid = request.POST['woeid']
        print(woeid)
    data = getTrends(int(woeid))
    for item in data:
        item["trend"] = item["_id"]
        del item["_id"]
    d = {"woeid": woeid, "data": data}
    print("sending response")

    return HttpResponse(json.dumps(d), content_type='application/json')


@csrf_exempt
def tweets(request):
    """
    :param request:
    :return:
    """
    print("views.tweets()")
    trend = request.POST['trend']
    woeid = int(request.POST['woeid'])
    print(trend + " " + str(woeid))
    data = getTweets(trend, woeid)
    print("redirecting to tweets.html")
    return render(request, 'tweets/tweets.html', {"data": data})
