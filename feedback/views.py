import boto3
from uuid import uuid4
from django.conf import settings
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *
from rest_framework.exceptions import ValidationError
from botocore.exceptions import ClientError, NoCredentialsError

class FeedbackUploadViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateFeedbackSerializer
    queryset = Feedback.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'id'

    def perform_create(self, serializer):
        image = self.request.FILES.get('feedback_image')
        image_url = None

        if image:
            try:
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
            except (ClientError, NoCredentialsError) as e:
                raise ValidationError({"feedback_image": "S3 업로드 실패", "detail": str(e)})

        serializer.save(feedback_image_url=image_url)

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

class Feedback_search_view(generics.ListAPIView):
    serializer_class = CreateFeedbackSerializer
    pagination_class = None

    def get_queryset(self):
        qs = Feedback.objects.all()
        keyword = (self.request.query_params.get("keyword") or "").strip()
        if not keyword:
            return qs.none()
        return qs.filter(ai_keyword__icontains=keyword).order_by("-id")
