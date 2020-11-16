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

class indexView(View):
    
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/dashboard')
        context = {}
        return render(request, "index.html", {"context": context})


class dashboardView(LoginRequiredMixin, View):
    
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


class loginView(FormView):
    form_class = AuthenticationForm
    template_name = "login.html"
    success_url = "/dashboard"

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/dashboard')
        return super(loginView, self).get(request, *args, **kwargs)

class logoutView(RedirectView):
    url = '/'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(logoutView, self).get(request, *args, **kwargs)


class registerView(FormView):
    form_class = UserCreationForm
    template_name = "register.html"
    success_url = "/login"

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class resolverView(View):
    
    def get(self,request, *args, **kwargs):
        print("kwargs:",kwargs)
        urlDo = get_object_or_404(UrlList, shortUrl=kwargs['shortUrl'])
        url = urlDo.longUrl
        if not "://" in url:
            url = 'http://'+url
        print("Redirecting to :",url)
        print("Time : ", datetime.datetime.now())
        print("IP:", get_client_ip(request))
        print("Useragent:",request.META['HTTP_USER_AGENT'])
        AnalyticsDo = AnalyticsList(user = urlDo.user, ip = get_client_ip(request), userAgent = request.META['HTTP_USER_AGENT'], accessedOn= datetime.datetime.now(), shortUrl=kwargs['shortUrl'])
        AnalyticsDo.save()

        return redirect(url)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

class analyticsView(LoginRequiredMixin, View):
    def get(self, request):
        context = {}
        items = AnalyticsList.objects.filter(user = request.user)
        context["items"] = items
        return render(request, "analytics.html", context)