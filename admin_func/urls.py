from django.urls import path
from .views import *
from walktrails.views import Walktrail_route, Walktrail_feedback

app_name = 'admin_func'
urlpatterns = [
    path('notice/', FeedbackinProgress.as_view(), name='feedback_notice'),
    path('route/<str:walktrail_name>/', Walktrail_route.as_view(), name='walktrail_route'),
    path('feedback/<str:walktrail_name>/<str:type>/', Walktrail_feedback.as_view(), name='walktrail_feedback'),
    path('current/<str:walktrail_name>/', CurrentFeedback.as_view(), name='current_feedback'),    
    path('create/<int:pk>/', ResponseCreateView.as_view(), name='response-create'),
    path('responed/<str:walktrail_name>/', RespondedFeedbackView.as_view(), name='responded-feedback-list'),
]