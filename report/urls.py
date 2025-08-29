from django.urls import path

from .views import Custom_AI_report_view

app_name = 'report'
urlpatterns = [
    path('custom/', Custom_AI_report_view.as_view()),
]