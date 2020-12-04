from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from urlShortenerApp.models import UrlList, AnalyticsList
from rest_framework import viewsets, generics, mixins
from .serializers import UrlListSerializer, AnalyticsListSerializer
from django.shortcuts import get_object_or_404, redirect
from django.contrib.gis.geoip2 import GeoIP2
from django.utils import timezone
from django.http import HttpResponseNotFound
import datetime
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class DashboardApiViewSet(viewsets.ModelViewSet):
    serializer_class = UrlListSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "shortUrl"
    def get_queryset(self):
        return UrlList.objects.filter(user=self.request.user)
    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

class AnalyticsApiViewSet(viewsets.ModelViewSet):
    serializer_class = AnalyticsListSerializer
    lookup_field = "shortUrl"
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return AnalyticsList.objects.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        queryset = AnalyticsList.objects.filter(user=self.request.user, shortUrl=kwargs['shortUrl'])
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class ResolverApiView(viewsets.ReadOnlyModelViewSet):
    lookup_field = "shortUrl"
    queryset = UrlList.objects.all()
    serializer_class = UrlListSerializer
    def retrieve(self, request, *args, **kwargs):
        urlDo = get_object_or_404(UrlList, shortUrl=kwargs['shortUrl'])
        serializer = self.get_serializer(urlDo)
        
        currentTime = timezone.now()
        print(currentTime)
        expiryDatetime = urlDo.expiryDatetime
        print(expiryDatetime)
        if expiryDatetime != None and expiryDatetime > currentTime :
            url = urlDo.longUrl
            if not "://" in url:
                url = 'http://'+url
            print("Redirecting to :",url)
            print("Time : ", datetime.datetime.now())
            ip = get_client_ip(request)
            print("IP:", ip)
            print("Useragent:",request.META['HTTP_USER_AGENT'])

            device_type = ""
            browser_type = ""
            browser_version = ""
            os_type = ""
            os_version = ""
            if request.user_agent.is_mobile:
                device_type = "Mobile"
            if request.user_agent.is_tablet:
                device_type = "Tablet"
            if request.user_agent.is_pc:
                device_type = "PC"
            
            browser_type = request.user_agent.browser.family
            browser_version = request.user_agent.browser.version_string
            os_type = request.user_agent.os.family
            os_version = request.user_agent.os.version_string

            location_country = None
            location_city = None

            try:
                g = GeoIP2()
                location = g.city(ip)
                location_country = location["country_name"]
                location_city = location["city"]
            except:
                print("Address Not found")

            AnalyticsDo = AnalyticsList(
                user = urlDo.user, 
                ip = ip,
                userAgent = request.META['HTTP_USER_AGENT'], 
                accessedOn= datetime.datetime.now(), 
                shortUrl=kwargs['shortUrl'],
                deviceType = device_type,
                browserType = browser_type,
                browserVersion = browser_version,
                osType = os_type,
                osVersion = os_version,
                country = location_country, 
                city = location_city)
            AnalyticsDo.save()
            return redirect(serializer.data['longUrl'])
        else:
            return HttpResponseNotFound("<h1>Link expired</h1>")



def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

class DetailedAnalyticsApiView(LoginRequiredMixin ,TemplateView):
   template_name = 'analytics2.html'

   def get_context_data(self, **kwargs):
       context = super(DetailedAnalyticsApiView, self).get_context_data(**kwargs)
       context['currentTime'] = timezone.now()
       return context