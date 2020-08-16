from django.urls import path
from . import views

urlpatterns = [
    path('', views.spectrum, name='spectrum'),
    path('left/', views.left, name='spectrum-left'),
    path('center/', views.center, name='spectrum-center'),
    path('right/', views.right, name='spectrum-right'),
]
