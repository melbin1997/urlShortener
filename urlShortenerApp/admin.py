from django.contrib import admin
from . import models

class UrlListAdmin(admin.ModelAdmin):
    list_display=("user", "longUrl", "shortUrl")
class AnalyticsListAdmin(admin.ModelAdmin):
    list_display=("user", "shortUrl", "accessedOn", "ip", "userAgent")

admin.site.register(models.UrlList, UrlListAdmin)
admin.site.register(models.AnalyticsList, AnalyticsListAdmin)
