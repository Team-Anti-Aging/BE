from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'upload', FeedbackUploadViewSet, basename='feedback-upload')

urlpatterns = [
    path('<int:id>/', GetFeedback.as_view(), name='feedback-get'),
    path('search/', Feedback_search_view.as_view())
] + router.urls