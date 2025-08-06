from rest_framework import generics, permissions
from django.db.models import Count, Q
from rest_framework.response import Response as DRFResponse

from . import serializers
from . import models

# Create your views here.
class GetRouteAll(generics.ListAPIView):
    # 전체 산책로 좌표정보 받아오기 / 관리자용
    queryset = models.WalkTrail.objects.all()
    serializer_class = serializers.WalkTrailRouteSerializer
    pagination_class = None

class WalkTrail_list(generics.ListAPIView):
    # walktrail 리스트 조회
    queryset = models.WalkTrail.objects.all()
    serializer_class = serializers.WalkTrailListSerializer
    pagination_class = None

class WalkTrail_info(generics.RetrieveAPIView):
    # 특정 산책로 정보 조회
    queryset = models.WalkTrail.objects.all()
    serializer_class = serializers.WalkTrailInfoSerializer
    lookup_field = 'name'
    lookup_url_kwarg = 'name'

class WalkTrail_list_count(generics.GenericAPIView):
    permission_classes = [permissions.IsAdminUser]  # 관리자만 접근 가능

    def get(self, request):
        # 각 WalkTrail 별로 미처리된 Feedback 개수 계산
        result = (
            models.WalkTrail.objects.annotate(
                total_count=Count('feedback'),
                incomplete_count=Count('feedback', filter=Q(feedback__status='in_progress')),
                completed_count=Count('feedback', filter=Q(feedback__status='completed')),
            )
            .values('name', 'total_count', 'incomplete_count',  'completed_count')
        )
        return DRFResponse(result)

