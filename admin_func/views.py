import boto3
from uuid import uuid4
from django.conf import settings
from rest_framework import generics, permissions
from .models import *
from .serializers import *
from feedback.models import Feedback, WalkTrail
from django.db.models import Count, Q
from rest_framework.response import Response as DRFResponse
from admin_func.models import Response as ResponseModel

class IncompleteFeedbackPerTrailView(generics.ListAPIView):
    serializer_class = ResponseListSerializer
    permission_classes = [permissions.IsAdminUser]  # 관리자만 접근 가능

    def get(self, request):
        # 각 WalkTrail 별로 미처리된 Feedback 개수 계산
        result = (
            WalkTrail.objects.annotate(
                total_count=Count('feedback'),
                incomplete_count=Count('feedback', filter=Q(feedback__status='in_progress')),
                completed_count=Count('feedback', filter=Q(feedback__status='completed')),
            )
            .values('name', 'total_count', 'incomplete_count',  'completed_count')
        )
        return DRFResponse(result)

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
            # presigned URL 생성
            presigned_url = s3.generate_presigned_url(
                'get_object',
                Params={'Bucket': bucket_name, 'Key': file_key},
                ExpiresIn=3600  # 1시간 유효
            )   

            image_url = presigned_url
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
        return Response.objects.filter(
            feedback__walktrail__name=walktrail_name,
            feedback__status='completed'
        ).order_by('-responded_at')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return DRFResponse(serializer.data)