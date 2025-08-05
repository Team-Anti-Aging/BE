from django.urls import path
from .views import *

urlpatterns = [
    path('upload/', FeedbackUploadView.as_view(), name='feedback-upload'),
    path('list/<str:walktrail_name>/', RespondedFeedback.as_view(), name='feedback-list-walktrail'),
    path('list/<str:walktrail_name>/<str:type>/', FeedbackListByType.as_view(), name='feedback-list-walktrail-type'),
]