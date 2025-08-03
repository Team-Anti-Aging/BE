from django.contrib import admin
from django.urls import path

from . import views

app_name = 'walktrails'
urlpatterns = [
    path('', views.GetRouteAll.as_view(), name='GetRouteAll'),
    path('list/', views.WalkTrail_list.as_view(), name='walktrail_list'),
    path('<str:name>/', views.WalkTrail_info.as_view(), name='walktrail_info'),
]