from django.urls import path
from .views import *

app_name = 'admin_func'
urlpatterns = [
    path('create/<int:pk>/', ResponseCreateView.as_view(), name='response-create'),
    path('responded/<str:walktrail_name>/', RespondedFeedbackView.as_view(), name='responded-feedback-list'),
]