from django.db import models
from django.contrib.auth.models import User
import random, string


class UrlList(models.Model):
    user = models.ForeignKey(User, verbose_name="username", on_delete=models.CASCADE)
    longUrl = models.TextField(max_length=500)
    shortUrl = models.TextField(max_length=200)
    expiryDatetime = models.DateTimeField(auto_now=False, auto_now_add=False, null=True)

    def __str__(self):
        return self.longUrl

    def save(self, *args, **kwargs):
        x = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
        # Checks if short link is already in DB, if present then generates another link
        while UrlList.objects.filter(shortUrl = x).first() != None:
            x = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
        self.shortUrl = x
        return super(UrlList, self).save(*args, **kwargs)

class AnalyticsList(models.Model):
    user = models.ForeignKey(User, verbose_name="username", on_delete=models.CASCADE)
    shortUrl = models.TextField(max_length=200, default="null")
    accessedOn = models.DateTimeField(auto_now=True)
    ip = models.TextField(max_length=40)
    userAgent = models.TextField(max_length=200)
    deviceType = models.TextField(max_length=50, null=True)
    browserType = models.TextField(max_length=50, null=True)
    browserVersion = models.TextField(max_length=50, null=True)
    osType = models.TextField(max_length=50, null=True)
    osVersion = models.TextField(max_length=50, null=True)
    country = models.TextField(max_length=50, null=True)
    city = models.TextField(max_length=50, null=True)

    def __str__(self):
        return self.shortUrl

    class Meta:
        ordering = ['-id']
