from django.urls import path
from .views import *

urlpatterns = [
    path('upload/', FeedbackUploadView.as_view(), name='feedback-upload'),
    path('list/<str:walktrail_name>/<str:type>/<str:status>/', AllFeedback.as_view(), name='feedback-list-walktrail'), #status 종류별로 분기
    path('<int:id>/', GetFeedback.as_view(), name='feedback-get'),
]