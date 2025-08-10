from django.contrib import admin
from django.urls import path

from . import views

app_name = 'walktrails'
urlpatterns = [
    # path('', views.GetRouteAll.as_view(), name='GetRouteAll'),
    path('list/', views.Walktrail_list.as_view(), name='walktrail_list'),
    path('route/<str:walktrail_name>/', views.Walktrail_route.as_view(), name='walktrail_route'),
    path('feedback/<str:walktrail_name>/<str:type>/', views.Walktrail_feedback.as_view(), name='walktrail_feedback'),
    path('info/<str:walktrail_name>/', views.Walktrail_info.as_view(), name='walktrail_info'),
    path('list/count/', views.WalkTrail_list_count.as_view(), name='walktrail_list_count'),
]