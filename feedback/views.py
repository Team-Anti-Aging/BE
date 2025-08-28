import boto3
from uuid import uuid4
from django.conf import settings
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *
from openai import OpenAI
from decouple import config
from rest_framework.exceptions import ValidationError
from botocore.exceptions import ClientError, NoCredentialsError

# 재준이형꺼
def run_ai_analysis(content):
    system ="""
    당신은 산책로 민원 데이터를 처리하는 공무원입니다.
    아래 “민원 원문”을 분석하여, 지정된 JSON 스키마에 맞춰 결과만 반환하세요.
    반드시 유효한 JSON만 출력하세요. 불필요한 텍스트는 출력하지 마세요.
    
    [제약]
    - ai_keyword: 한 단어만.
    - ai_situation: 문제 상황을 적어주고, 없으면 null로
    - ai_demand: 요구사항을 적어주고, 없으면 null로
    - ai_importance: "높음" | "중간" | "낮음" (높음: 안전 관련 / 중간: 불편하지만 긴급하진 않음 / 낮음: 개선되면 좋지만 시급하지 않음)
    - ai_expected_duration: "긴급" | "단기" | "중장기".
    - ai_solution: 실행 가능한 조치 1문장만.
    - ai_note: 그 외 특이사항, 없으면 null
    }
    """
    api_key = config("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.1,
        response_format={"type": "json_object"},  # 무조건 JSON만 나오게 강제
        messages=[
        {"role": "system", "content": system},
        {"role": "user", "content": content},
        ],
    )
    return resp

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
