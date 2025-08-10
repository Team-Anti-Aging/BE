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
        user = self.context['request'].user
        validated_data.pop('feedback_image',None)
        return Feedback.objects.create(user=user, **validated_data)
    
class OnlyFeedbackSerializer(serializers.ModelSerializer):
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
        ]
        read_only_fields = [
            'id',
            'created_at',
            'updated_at',
        ]