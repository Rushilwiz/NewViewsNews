# Create your models here.
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Article(models.Model):
    content = models.TextField()
    date_published = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.author}'s article on {self.date_published}"

    def get_absolute_url(self):
        return reverse('article-detail', kwargs={'pk': self.pk})
