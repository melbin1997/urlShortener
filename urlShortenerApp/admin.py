from django.contrib import admin
from . import models

class UrlListAdmin(admin.ModelAdmin):
    list_display=("user", "longUrl", "shortUrl")

admin.site.register(models.UrlList, UrlListAdmin)
