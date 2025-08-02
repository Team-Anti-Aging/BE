from django.contrib import admin
from django.urls import path

from . import views

app_name = 'walktrails'
urlpatterns = [
    path('', views.GetRouteAll.as_view(), name='GetRouteAll'),
    path('list/', views.WalkTrail_list.as_view(), name='walktrails_list'),
    path('<str:name>/', views.GetRoute.as_view(), name='GetRoute'),
    path('<str:name>/info/', views.WalkTrail_info.as_view(), name='walktrails_info'),    # 각 산책로
]