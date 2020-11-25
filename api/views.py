from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from urlShortenerApp.models import UrlList
from rest_framework import viewsets
from .serializers import UrlListSerializer


class DashboardApiViewSet(viewsets.ModelViewSet):
    serializer_class = UrlListSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "shortUrl"
    def get_queryset(self):
        return UrlList.objects.filter(user=self.request.user)
    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)