from urlShortenerApp.models import UrlList
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
    