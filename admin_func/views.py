import boto3
from uuid import uuid4
from django.conf import settings
from rest_framework import generics, permissions
from .models import *
from .models import Response as ResponseModel
from .serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView
from feedback.models import Feedback, WalkTrail
from django.db.models import Count, Q, F
from django.utils.timezone import now
from feedback.serializers import OnlyFeedbackSerializer

# 각 산책로별 피드백 현황
class FeedbackinProgress(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        qs = WalkTrail.objects.annotate(
            unresolved_count=Count('feedback', filter=Q(feedback__status='in_progress')),            
        ).values('name', 'unresolved_count')
        return Response(list(qs))
    
# 각 산책로별 피드백 리스트 (상위 5개)
class CurrentFeedbackList(generics.ListAPIView):
    serializer_class = CurrentFeedbackSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        walktrail_name = self.kwargs.get('walktrail_name')
        qs = WalkTrail.objects.filter(feedback__status='in_progress', name=walktrail_name)
        # 피드백의 생성시간 기준 내림차순 정렬, 상위 5개
        return qs.order_by('-feedback__created_at')

# 산책로 현황 기본 화면
class EntireFeedbackView(generics.ListAPIView):
    serializer_class = FeedbackSummarySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WalkTrail.objects.values('name').annotate(
            suggestion_count=Count('feedback', filter=Q(feedback__type='제안')),
            inconvenience_count=Count('feedback', filter=Q(feedback__type='불편'))
        ).order_by('id')

#산책로별 상세 현황
class FeedbackByTrailView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FeedbackCategoryCountSerializer

    def get(self, request, walktrail_name):
        qs = Feedback.objects.filter(walktrail__name=walktrail_name).values(
            'walktrail__name', 'type'
        ).annotate(
            count_category1=Count(
                'id',
                filter=Q(type='불편', category='안전') | Q(type='제안', category='편의시설 확충')
            ),
            count_category2=Count(
                'id',
                filter=Q(type='불편', category='청결') | Q(type='제안', category='경관 개선')
            ),
            count_category3=Count(
                'id',
                filter=Q(type='불편', category='이동성') | Q(type='제안', category='정보 제공')
            ),
            count_category4=Count(
                'id',
                filter=Q(type='불편', category='소음방해') | Q(type='제안', category='프로그램/이벤트')
            )


        ).order_by('walktrail__name','type')

        return Response(FeedbackCategoryCountSerializer(qs, many=True).data)

# 금일 신고 내역 (산책로 별 / (불편, 제안) 별)
# ==============================================================================================
class TodayFeedbackView(generics.ListAPIView):
    serializer_class=CurrentFeedbackSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        today = now().date()
        qs = Feedback.objects.filter(created_at__date=today).values(
            'walktrail__name', 'type'
        ).annotate(count=Count('id')).order_by('walktrail__name', 'type')
        return Response(list(qs))

# 특정 산책로의 최근 피드백
class RecentFeedbackView(generics.ListAPIView):
    serializer_class = OnlyFeedbackSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        walktrail_name = self.kwargs.get('walktrail_name')
        pk = self.kwargs.get('pk')  # 선택적으로 들어올 수 있음
        qs = Feedback.objects.filter(walktrail__name=walktrail_name, status='in_progress')

        if pk is not None:
            qs = qs.filter(pk=pk)  # 특정 feedback 하나만
        else:
            qs = qs.order_by('-created_at')  # 리스트일 경우 최신순

        return qs
    
# ============================================================================================================
# 피드백에 대한 응답 생성 뷰
class ResponseCreateView(generics.CreateAPIView):
    queryset = ResponseModel.objects.all()
    serializer_class = ResponseCreateSerializer
    permission_classes = [permissions.IsAdminUser]  # 관리자만 접근 가능

    def perform_create(self, serializer):
        pk= self.kwargs.get('pk')
        feedback = Feedback.objects.get(pk=pk)

        image = self.request.FILES.get('response_image')
        image_url = None

        if image:
            s3 = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_S3_REGION_NAME,
            )
            bucket_name = settings.AWS_STORAGE_BUCKET_NAME
            region = settings.AWS_S3_REGION_NAME

            ext = image.name.split('.')[-1]
            file_key = f"response_images/{uuid4()}.{ext}"

            s3.upload_fileobj(
                image, 
                bucket_name, 
                file_key,
                ExtraArgs={'ContentType': image.content_type}
            )

            image_url = f"https://{bucket_name}.s3.amazonaws.com/{file_key}"
            serializer.save(response_image_url=image_url)
        else:   
            serializer.save()

        response = serializer.save(admin=self.request.user)
        feedback.status = response.status
        feedback.save()
    

class RespondedFeedbackView(generics.ListAPIView):
    serializer_class = RespondedFeedbackSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        walktrail_name = self.kwargs.get('walktrail_name')
        return ResponseModel.objects.filter(  # 모델로 변경
            feedback__walktrail__name=walktrail_name,
            feedback__status='completed'
        ).order_by('-responded_at')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)  # DRF 응답 객체로 반환