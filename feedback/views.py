import boto3
from uuid import uuid4
from django.conf import settings
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *

class FeedbackUploadView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Feedback.objects.all()
    serializer_class = CreateFeedbackSerializer

    def perform_create(self, serializer):
        image = self.request.FILES.get('feedback_image')
        image_url = None

        if image:
            # boto3 클라이언트 설정
            s3 = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_S3_REGION_NAME,
            )

            bucket_name = settings.AWS_STORAGE_BUCKET_NAME
            region = settings.AWS_S3_REGION_NAME

            # 고유한 파일명 구성
            ext = image.name.split('.')[-1]
            file_key = f"feedback_images/{uuid4()}.{ext}"

            # S3에 파일 업로드 (기본 private로)
            s3.upload_fileobj(
                image,
                bucket_name,
                file_key,
                ExtraArgs={'ContentType': image.content_type}
            )

            image_url = f"https://{bucket_name}.s3.amazonaws.com/{file_key}"
            serializer.save(feedback_image_url=image_url)
        else:
            serializer.save()

class GetFeedback(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FeedbackSerializer
    queryset = Feedback.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'id'

# UnrespondedFeedback View
class AllFeedback(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FeedbackSerializer
    
    def get_queryset(self):
        walktrail_name = self.kwargs.get('walktrail_name')
        status = self.kwargs.get('status')
        type = self.kwargs.get('type')
        return Feedback.objects.filter(walktrail__name=walktrail_name, status=status, type=type).order_by('-created_at')
