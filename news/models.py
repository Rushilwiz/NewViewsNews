# Create your models here.
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

from PIL import Image

# Create your models here.

class Article(models.Model):
    headline = models.CharField(max_length=100)
    content = models.TextField()
    date_published = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    header = models.ImageField(default='default-header.jpg', upload_to='article-headers')
    header_caption = models.CharField(max_length=100, default="")

    def __str__(self):
        return f"{self.author}'s article on {self.date_published}"

    def get_absolute_url(self):
        return reverse('article-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.header.path)

        if img.width > 1280 or img.height > 768:
            output_size = (1280, 768)
            img.thumbnail(output_size)
            img.save(self.header.path)
