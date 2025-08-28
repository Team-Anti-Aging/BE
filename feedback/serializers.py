# feedback/serializers.py

from rest_framework import serializers
from .models import Feedback
from admin_func.serializers import ResponseDetailSerializer
from uuid import uuid4
from walktrails.models import WalkTrail

class FeedbackSerializer(serializers.ModelSerializer):
    #responses = ResponseDetailSerializer(many=True, read_only=True)

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
            # 'responses', # 역참조
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
    walktrail = serializers.SlugRelatedField(
        queryset=WalkTrail.objects.all(),
        slug_field="name"
    )
    
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
            'feedback_image_url',
            'created_at',
            'updated_at',
            'status',
            # AI
            'ai_keyword',
            'ai_situation',
            'ai_demand',
            'ai_importance',
            'ai_expected_duration',
            'ai_solution',
            'ai_note'
        ]
        read_only_fields = ('id', 'user', 'feedback_image_url', 'created_at', 'updated_at', 'status')

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        validated_data.pop('feedback_image',None)
        return Feedback.objects.create(**validated_data)
    
# class FeedbackAISerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Feedback
#         fields = [
#             'ai_keywords',
#             'ai_summary',
#             'ai_type',
#             'ai_importance',
#             'ai_expected_duration',
#             'ai_solution',
#             'ai_note',
#         ]
#         read_only_fields = []

# class UploadFeedbackSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Feedback
#         fields = [
#             'content',
#             'ai_category',
#             'ai_keywords',
#             'ai_type',
#             'ai_summary',
#         ]
#         read_only_fields = ['content']

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
            'ai_keywords',
            'ai_situation',
            'ai_demand',
            'ai_importance',
            'ai_expected_duration',
            'ai_solution',
            'ai_note'
        ]
        read_only_fields = [
            'id',
            'created_at',
            'updated_at',
        ]