from urlShortenerApp.models import UrlList, AnalyticsList
from rest_framework import serializers


class UrlListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UrlList
        fields = ['user','longUrl','shortUrl','expiryDatetime']
        extra_kwargs = {
                'shortUrl': {
                    'required': False
                 }
            }
    
class AnalyticsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalyticsList
        fields = ['user','shortUrl','accessedOn','ip','userAgent','deviceType','browserType','browserVersion','osType','osVersion','country','city']