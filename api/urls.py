
from django.contrib import admin
from django.urls import path
from .views import DashboardApiView

urlpatterns = [
    path('dashboard/', DashboardApiView.as_view({'get':'list','post':'create'}), name='dashboardApi'),
]
