from django.shortcuts import render

# Create your views here.

def about (request):
    return render (request, 'news/about.html')

def home (request):
    return render (request, 'news/home.html')
