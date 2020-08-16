# Create your models here.
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

from PIL import Image

from ckeditor.fields import RichTextField

# Create your models here.


class Article(models.Model):
    A_L = 'authoritarian_left'
    A_R = 'authoritarian_right'
    L_L = 'libertarian_left'
    L_R = 'libertarian_right'
    POLITICAL_CHOICES = [
        (A_L, ('Authoritarian Left')),
        (A_R, ('Authoritarian Right')),
        (L_L, ('Libertarian Left')),
        (L_R, ('Libertarian Right')),
    ]

    headline = models.CharField(max_length=100)
    # content = TextField()
    content = RichTextField(blank=True, null=True)
    date_published = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name="article_likes")
    header = models.ImageField(null=True, blank=True, default='default-header.jpg', upload_to='article-headers')
    header_caption = models.CharField(max_length=100, default="")
    tag = models.CharField(max_length=19,choices=POLITICAL_CHOICES,default=L_L)

    def __str__(self):
        return f"{self.headline} by {self.author}"

    def total_likes(self):
        return self.likes.count();

    def get_absolute_url(self):
        return reverse('article-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.header.path)

        if img.width > 1280 or img.height > 768:
            output_size = (1280, 768)
            img.thumbnail(output_size)
            img.save(self.header.path)
