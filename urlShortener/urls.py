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
from django.urls import path
from urlShortenerApp.views import indexView, loginView, registerView, dashboardView, logoutView, resolverView,analyticsView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', indexView.as_view(), name='index'),
    path('login/', loginView.as_view(), name="login"),
    path('register/', registerView.as_view(), name="register"),
    path('dashboard/', dashboardView.as_view(), name="dashboard"),
    path('analytics/', analyticsView.as_view(), name="analytics"),
    path('logout/', logoutView.as_view(), name="logout"),
    path('short/<str:shortUrl>', resolverView.as_view(), name="resolver")
]
