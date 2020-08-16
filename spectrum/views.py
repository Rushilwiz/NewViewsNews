from django.shortcuts import render
import feedparser
# Create your views here.

def spectrum(request):
    return render(request, "spectrum/home.html")


def right(request):
    feed = feedparser.parse("http://feeds.foxnews.com/foxnews/politics")
    print(feed.entries)
    context = {
        "feed": feed.entries
    }
    return render (request, "spectrum/feed.html", context)


def left(request):
    feed = feedparser.parse("https://rss.app/feeds/xC2p60TEA2cjxsTp.xml")
    print(feed.entries)
    context = {
        "feed": feed.entries
    }
    return render (request, "spectrum/feed.html", context)

def center(request):
    feed = feedparser.parse("https://rss.app/feeds/H4872WxBBmcWNjWr.xml")
    print(feed.entries)
    context = {
        "feed": feed.entries
    }
    return render (request, "spectrum/feed.html", context)
