"""urlShortener URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from urlShortenerApp.views import IndexView, LoginView, RegisterView, DashboardView, LogoutView, ResolverView,AnalyticsView,DetailedAnalyticsView
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from api.views import DetailedAnalyticsApiView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('login/', LoginView.as_view(), name="login"),
    path('register/', RegisterView.as_view(), name="register"),
    path('dashboard/', DashboardView.as_view(), name="dashboard"),
    path('analytics/<str:shortUrl>', DetailedAnalyticsView.as_view(), name="detailedAnalytics"),
    path('analytics/', AnalyticsView.as_view(), name="analytics"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('short/<str:shortUrl>', ResolverView.as_view(), name="resolver"),
    path('dashboard2/', login_required(TemplateView.as_view(template_name='dashboard2.html')), name="dashboard2"),
    path('analytics2/<str:shortUrl>', DetailedAnalyticsApiView.as_view()),
    path('analytics2/', login_required(TemplateView.as_view(template_name='analytics2.html')), name="analytics2"),
    path('api/', include('api.urls')),
    path('chooseDashboard/', login_required(TemplateView.as_view(template_name='chooseDashboard.html')), name="chooseDashboard"),
]
