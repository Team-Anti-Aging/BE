import boto3
from uuid import uuid4
from django.conf import settings
# Create your views here.
from rest_framework import generics, permissions
from .models import *
from .serializers import *
from feedback.models import Feedback

class ResponseCreateView(generics.CreateAPIView):
    queryset = Response.objects.all()
    serializer_class = ResponseCreateSerializer
    permission_classes = [permissions.IsAdminUser]  # 관리자만 접근 가능

    def perform_create(self, serializer):

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
        feedback = response.feedback
        feedback.status = response.status
        feedback.save()

class ResponseListView(generics.ListAPIView):
    queryset = Response.objects.all()
    serializer_class = ResponseListSerializer
    permission_classes = [permissions.IsAdminUser]  # 관리자만 접근 가능
