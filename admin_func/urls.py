from django.urls import path
from .views import *

app_name = 'admin_func'
urlpatterns = [
    path('', FeedbackinProgress.as_view(), name='feedback-in-progress'),
    path('route/<str:route>/', FeedbackperRoute.as_view(), name='feedback-per-route'),
    path('create/<int:pk>/', ResponseCreateView.as_view(), name='response-create'),
    path('responded/<str:walktrail_name>/', RespondedFeedbackView.as_view(), name='responded-feedback-list'),
]