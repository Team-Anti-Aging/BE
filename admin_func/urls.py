from django.urls import path
from .views import *

urlpatterns = [
    path('responses/create/', ResponseCreateView.as_view(), name='response-create'),
    path('responses/', ResponseListView.as_view(), name='response-list'),
]