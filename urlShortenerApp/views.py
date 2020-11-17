from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import FormView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from .models import UrlList, AnalyticsList
import random, string
from django.http import HttpResponseRedirect
from django.http import HttpResponse
import logging
import datetime
from django.contrib.gis.geoip2 import GeoIP2
from django.views.generic import ListView

class IndexView(View):
    
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/dashboard')
        context = {}
        return render(request, "index.html", {"context": context})


class DashboardView(LoginRequiredMixin, View):
    
    def get(self, request):
        context = {}
        urls = UrlList.objects.filter(user = request.user)
        context["urls"] = urls
        return render(request, "dashboard.html", context)

    def post(self, request):
        context = {}
        longUrl = request.POST["longUrl"]
        print("longURL : ", longUrl)
        x = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
        urlDo = UrlList(user = request.user, longUrl = longUrl, shortUrl = x)
        urlDo.save()
        urls = UrlList.objects.filter(user = request.user)
        context["urls"] = urls
        return render(request, "dashboard.html", context)


class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = "login.html"
    success_url = "/dashboard"

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/dashboard')
        return super(LoginView, self).get(request, *args, **kwargs)

class LogoutView(RedirectView):
    url = '/'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class RegisterView(FormView):
    form_class = UserCreationForm
    template_name = "register.html"
    success_url = "/login"

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class ResolverView(View):
    
    def get(self,request, *args, **kwargs):
        print("kwargs:",kwargs)
        urlDo = get_object_or_404(UrlList, shortUrl=kwargs['shortUrl'])
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

        return redirect(url)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

class AnalyticsView(LoginRequiredMixin, ListView):
    context_object_name = 'items'
    template_name = 'analytics.html'
    paginate_by = 13

    def get_queryset(self):
        return AnalyticsList.objects.filter(user=self.request.user)