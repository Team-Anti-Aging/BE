import boto3
from uuid import uuid4
from django.conf import settings
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *

class FeedbackUploadView(generics.CreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = CreateFeedbackSerializer
    permission_classes = [IsAuthenticated]

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

            # presigned URL 생성 (예: 1시간 유효)
            presigned_url = s3.generate_presigned_url(
                'get_object',
                Params={'Bucket': bucket_name, 'Key': file_key},
                ExpiresIn=3600  # 3600초 = 1시간
            )

            image_url = presigned_url
            serializer.save(feedback_image_url=image_url)
        else:
            serializer.save()

class FeedbackListByWalktrail(generics.ListAPIView):
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        walktrail_name = self.kwargs.get('walktrail_name')
        return Feedback.objects.filter(walktrail__name=walktrail_name)

class FeedbackListByType(generics.ListAPIView):
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        walktrail_name = self.kwargs.get('walktrail_name')
        feedback_type = self.kwargs.get('type')
        return Feedback.objects.filter(walktrail__name=walktrail_name, type=feedback_type)