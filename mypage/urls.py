from django.urls import path

from .views import Favorite_walktrail_view, Favorite_walktrail_list_view, Mypage_view, Feedback_list_view

app_name = 'mypage'
urlpatterns = [
    path('count/', Mypage_view.as_view()),
    path('favorite/post/<str:walktrail_name>/', Favorite_walktrail_view.as_view()),
    path('favorite/delete/<str:walktrail_name>/', Favorite_walktrail_view.as_view()),
    path('favorite/list/',Favorite_walktrail_list_view.as_view()),
    path('feedback/list/', Feedback_list_view.as_view()),
    
]