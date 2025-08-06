from django.urls import path
from .views import *

urlpatterns = [
    path('', IncompleteFeedbackPerTrailView.as_view(), name='incomplete-feedback-by-trail'),
    path('create/<int:pk>/', ResponseCreateView.as_view(), name='response-create'),
    path('responded/<str:walktrail_name>/', RespondedFeedbackView.as_view(), name='responded-feedback-list'),
]