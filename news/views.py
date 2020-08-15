from django.shortcuts import render
from users.models import Profile

# Create your views here.

def about (request):
    return render (request, 'news/about.html')

def home (request):
    if request.user.is_authenticated and Profile.objects.filter(user=request.user).count() < 1:
        Profile.objects.create(user=request.user).save()

    return render (request, 'news/home.html')
