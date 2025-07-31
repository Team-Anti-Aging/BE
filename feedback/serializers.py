from rest_framework import serializers

# feedback/serializers.py

from rest_framework import serializers
from .models import Feedback

class FeedbackSerializer(serializers.ModelSerializer):
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
            'feedback_image',
            'created_at',
            'updated_at',
            'admin',
            'status',
            'response_content',
            'responded_at',
            'response_image',
        ]
        read_only_fields = [
            'id',
            'created_at',
            'updated_at',
            'responded_at',
        ]

    def __str__(self):
        return f"Feedback #{self.instance.id} by {self.instance.user.nickname}" if self.instance else "Feedback Serializer"

# feedback/serializers.py
class CreateFeedbackSerializer(serializers.ModelSerializer):
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
        ]

    def create(self, validated_data):
        # 사용자(user)는 뷰에서 request.user로 설정
        user = self.context['request'].user
        return Feedback.objects.create(user=user, **validated_data)

class FeedbackResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = [
            'status',
            'response_content',
            'responded_at',
            'response_image',
        ]

    def update(self, instance, validated_data):
        admin = self.context['request'].user
        instance.admin = admin  # 관리자는 request.user로 설정
        instance.status = validated_data.get('status', instance.status)
        instance.response_content = validated_data.get('response_content', instance.response_content)
        instance.responded_at = validated_data.get('responded_at')
        instance.response_image = validated_data.get('response_image', instance.response_image)
        instance.save()
        return instance
