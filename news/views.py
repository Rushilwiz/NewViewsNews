from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .models import Article
from users.models import Profile


# Create your views here.

@login_required
def about (request):
    createProfileIfNotExist(request)
    if checkValues(request) is False:
        return redirect('values')

    return render (request, 'news/about.html')

def policy (request):
    return render (request, 'news/policy.html')

@login_required
def home (request):
    createProfileIfNotExist(request)
    if checkValues(request) is False:
        return redirect('values')

    profile = request.user.profile
    social = profile.socialScore
    economic = profile.economicScore

    A_L = 'authoritarian_left'
    A_R = 'authoritarian_right'
    L_L = 'libertarian_left'
    L_R = 'libertarian_right'

    if social > 0:
        # Auth
        if economic > 0:
            #AuthRight
            articles = Article.objects.exclude(tag=A_R)
        elif economic < 0:
            #AuthLeft
            articles = Article.objects.exclude(tag=A_L)
        else:
            #AuthCenter
            articles = Article.objects.exclude(tag=A_L).exclude(tag=A_R)
    elif social < 0:
        # Lib
        if social > 0:
            #LibRight
            articles = Article.objects.exclude(tag=L_R)
        elif social < 0:
            #LibLeft
            articles = Article.objects.exclude(tag=L_L)
        else:
            #LibCenter
            articles = Article.objects.exclude(tag=L_L).exclude(tag=L_R)
    else:
        #___Center
        if social > 0:
            # RightCenter
            articles = Article.objects.exclude(tag=L_L).exclude(tag=A_L)
        if social < 0:
            # LeftCenter
            articles = Article.objects.exclude(tag=L_R).exclude(tag=A_R)
        else:
            # Center
            articles = Article.objects.all()


    context = {
        'articles': articles
    }

    return render (request, 'news/home.html', context)

class ArticleListView(ListView):

    model = Article
    template_name = "news/home.html"
    context_object_name='articles'
    ordering = ['-date_published']
    paginate_by = 8

class UserArticleListView(ListView):
    model = Article
    template_name = "news/user_article.html"
    context_object_name='articles'
    paginate_by = 8

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Article.objects.filter(author=user).order_by('-date_published')

class ArticleDetailView(DetailView):
    model = Article

class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    fields=['headline','header','header_caption','content','tag']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    fields=['headline','header','header_caption','content','tag']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        article = self.get_object()
        return self.request.user == article.author

class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    success_url='/'

    def test_func(self):
        article = self.get_object()
        return self.request.user == article.author

def createProfileIfNotExist (request):
    if request.user.is_authenticated and Profile.objects.filter(user=request.user).count() < 1:
        Profile.objects.create(user=request.user).save()

def checkValues (request):
    if request.user.is_authenticated and Profile.objects.filter(user=request.user).count() is 1:
        profile = Profile.objects.filter(user=request.user).first()
        return profile.gaveValues
    return True
