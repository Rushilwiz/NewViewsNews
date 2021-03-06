from django.urls import path
from .views import (
    ArticleListView,
    ArticleDetailView,
    ArticleCreateView,
    ArticleUpdateView,
    ArticleDeleteView,
    UserArticleListView,
    LikeView,
)
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('policy/', views.policy, name='privacy-policy'),
    path('howto/', views.howto, name='howto'),

    path('user/<str:username>', UserArticleListView.as_view(), name='user-articles'),
    path('article/<int:pk>/', ArticleDetailView.as_view(), name='article-detail'),
    path('article/new/', ArticleCreateView.as_view(), name='article-create'),
    path('article/<int:pk>/update/', ArticleUpdateView.as_view(), name='article-update'),
    path('article/<int:pk>/delete/', ArticleDeleteView.as_view(), name='article-delete'),
    path('like/<int:pk>', LikeView, name='like_article')
]
