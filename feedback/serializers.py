# feedback/serializers.py

from rest_framework import serializers
from .models import Feedback
from admin_func.serializers import ResponseDetailSerializer
from uuid import uuid4

class FeedbackSerializer(serializers.ModelSerializer):
    responses = ResponseDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Feedback
        fields = [
            'id',
            'user',
            'walktrail',
            'location',
            'type',
            'category',
            'latitude',
            'longitude',
            'feedback_content',
            'feedback_image_url',
            'created_at',
            'updated_at',
            'status',
            'responses', # 역참조
        ]
        read_only_fields = [
            'id',
            'created_at',
            'updated_at',
        ]

    def __str__(self):
        return f"Feedback #{self.instance.id} by {self.instance.user.nickname}" if self.instance else "Feedback Serializer"

# feedback/serializers.py
class CreateFeedbackSerializer(serializers.ModelSerializer):
    feedback_image = serializers.ImageField(write_only=True, required=False)
    feedback_image_url = serializers.CharField(read_only=True)
    
    class Meta:
        model = Feedback
        fields = [
            'walktrail',
            'location',
            'type',
            'category',
            'latitude',
            'longitude',
            'feedback_content',
            'feedback_image',
            'feedback_image_url',
        ]
        read_only_fields = ('feedback_image_url',)

    def create(self, validated_data):
        # 사용자(user)는 뷰에서 request.user로 설정
        user = self.context['request'].user
        validated_data.pop('feedback_image',None)
        return Feedback.objects.create(user=user, **validated_data)


class RespondedFeedbackSerializer(serializers.ModelSerializer):
    walk_trail = serializers.SerializerMethodField()
    location = serializers.CharField()
    feedback_image_url = serializers.SerializerMethodField()
    response_image_url = serializers.SerializerMethodField()
    response_content = serializers.SerializerMethodField()

    class Meta:
        model = Feedback
        fields = [
            'walk_trail',
            'location',
            'feedback_image_url',
            'response_image_url',
            'response_content',
        ]

    def get_walk_trail(self, obj):
        return obj.walktrail.name if obj.walktrail else None

    def get_feedback_image_url(self, obj):
        return obj.feedback_image_url or None

    def get_response_content(self, obj):
        response = obj.responses.last()  # 가장 최근 응답을 기준으로 함
        return response.response_content if response else "No response content provided"

    def get_response_image_url(self, obj):
        response = obj.responses.last()
        return response.response_image_url if response else None
