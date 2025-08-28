from django.urls import path
from .views import *
from walktrails.views import Walktrail_route, Walktrail_feedback

app_name = 'admin_func'
urlpatterns = [
    path('notice/', FeedbackinProgress.as_view(), name='feedback_notice'), # 처리 중인 민원 갯수
    path('route/<str:walktrail_name>/', Walktrail_route.as_view(), name='walktrail_route'), # 산책로 경로 정보

    path('routefeedback/', EntireFeedbackView.as_view(), name='route_feedback_entire'), # 전체 산책로 피드백 현황
    path('routefeedback/<str:walktrail_name>/', FeedbackByTrailView.as_view(), name='route_feedback_specific'), #각 산책로별 피드백 카테고리 별 분포

    path('recent/', TodayFeedbackView.as_view(), name='today_feedback'), # 금일 피드백 현황 뷰
    path('recent/<str:walktrail_name>/', RecentFeedbackView.as_view(), name='recent_feedback'), # 특정 산책로의 최근 피드백 (전체)
    path('recent/<str:walktrail_name>/<int:pk>/', RecentFeedbackView.as_view(), name='recent_feedback_specific'), # 특정 산책로의 최근 피드백 (특정 1개)

    path('monthstats/<str:walktrail_name>/', MonthlyStatsView.as_view(), name='monthly_stats'),
    path('aireport/<str:walktrail_name>/', AIReportOpenAIView.as_view(), name='ai_report'),

    path('feedback/<str:walktrail_name>/', Walktrail_feedback.as_view(), name='walktrail_feedback'), # 각 산책로별 피드백 상세 리스트업 페이지
    path('current/<str:walktrail_name>/', CurrentFeedbackList.as_view(), name='current_feedback'), # 각 산책로별 피드백 리스트 (상위 5개) -> 필요할까요?
    
    path('create/<int:pk>/', ResponseCreateView.as_view(), name='response-create'), # 피드백에 대한 응답 생성
    path('responded/<str:walktrail_name>/', RespondedFeedbackView.as_view(), name='responded-feedback-list'), # 응답 완료된 피드백 리스트

]