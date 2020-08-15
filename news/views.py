from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
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

def about (request):
    createProfileIfNotExist(request)

    return render (request, 'news/about.html')

def home (request):
    createProfileIfNotExist(request)

    context = {
        'articles': Article.objects.all()
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
    fields=['headline','header','header_caption','content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    fields=['headline','header','header_caption','content']

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
