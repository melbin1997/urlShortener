from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import FormView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from .models import UrlList
import random, string
from django.http import HttpResponseRedirect
from django.http import HttpResponse
import logging

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
        x = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
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
        return redirect(url)
    # permanent = True
    # query_string = False
    # pattern_name = 'resolver'

    # def get_redirect_url(self, *args, **kwargs):
    #     print("hellooooooo")
    #     print("kwarg:", kwargs['shortUrl'])
    #     print("kwarg:", kwargs['shortUrl'])
    #     urlDo = UrlList.objects.get(shortUrl=kwargs['shortUrl'])
    #     # urlDo = get_object_or_404(UrlList, shortUrl=kwargs['shortUrl'])
    #     print("testing")
    #     print("urlDo", urlDo)
    #     url1 = urlDo.longUrl
    #     if not url1.contains("://"):
    #         url = 'http://'+url1
    #     else:
    #         print("false")
    #         url = url1
    #     print(url)
    #     return url
        # return super().get_redirect_url(*args, **kwargs)