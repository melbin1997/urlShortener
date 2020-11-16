from django.db import models
from django.contrib.auth.models import User

class UrlList(models.Model):
    user = models.ForeignKey(User, verbose_name="username", on_delete=models.CASCADE)
    longUrl = models.TextField(max_length=500)
    shortUrl = models.TextField(max_length=200)

    def __str__(self):
        return self.longUrl