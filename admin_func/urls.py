from django.urls import path
from .views import *

urlpatterns = [
    path('', IncompleteFeedbackPerTrailView.as_view(), name='incomplete-feedback-by-trail'),
    path('create/<int:pk>/', ResponseCreateView.as_view(), name='response-create'),
    path('responded/<int:pk>/', RespondedFeedbackView.as_view(), name='response-list'),
]