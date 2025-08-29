import boto3
from uuid import uuid4
from django.conf import settings
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *
from rest_framework.exceptions import ValidationError
from botocore.exceptions import ClientError, NoCredentialsError
from .services.ai_feedback import apply_ai_analysis_to_feedbacks

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

class FeedbackAIUpdateView(generics.UpdateAPIView):
    """
    기존 Feedback 데이터에 대해 AI 분석 결과를 업데이트합니다.
    """
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    lookup_field = 'id'  # URL에서 피드백 ID 기준

    def patch(self, request, *args, **kwargs):
        feedbacks = self.get_objects.all()  # id로 Feedback 가져오기

        for feedback in feedbacks:
            # AI 분석 실행
            ai_result = apply_ai_analysis_to_feedbacks(feedback.feedback_content)

        # AI 결과 필드 적용
        # ai_result는 JSON 형태라고 가정
        feedback.ai_keyword = ai_result.get("ai_keyword")
        feedback.ai_situation = ai_result.get("ai_situation")
        feedback.ai_demand = ai_result.get("ai_demand")
        feedback.ai_importance = ai_result.get("ai_importance")
        feedback.ai_expected_duration = ai_result.get("ai_expected_duration")
        feedback.ai_note = ai_result.get("ai_note")

        feedback.save()

        serializer = self.get_serializer(feedback)
        return Response(serializer.data, status=status.HTTP_200_OK)