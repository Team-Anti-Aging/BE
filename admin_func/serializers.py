from rest_framework import serializers
from .models import Response

class IncompleteFeedbackSerializer(serializers.Serializer):
    name = serializers.CharField()
    incomplete_count = serializers.IntegerField()


class ResponseDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response
        fields = [
            'admin',
            'feedback',
            'status',
            'response_content',
            'responded_at',
            'response_image_url',
        ]
        read_only_fields = [
            'id',
            'admin',
            'responded_at',
        ]


class ResponseCreateSerializer(serializers.ModelSerializer):
    response_image = serializers.ImageField(write_only=True, required=False)
    response_image_url = serializers.CharField(read_only=True)
    
    class Meta:
        model = Response
        fields = [
            'feedback',
            'status',
            'response_content',
            'response_image',
            'response_image_url',
        ]
        read_only_fields = ('response_image_url',)
    
    def create(self, validated_data):
        # 사용자(admin)는 뷰에서 request.user로 설정
        admin = self.context['request'].user
        validated_data.pop('response_image', None)
        response = Response.objects.create(admin=admin, **validated_data)
        return response


# 바뀐 동대문구에 전달할
class RespondedFeedbackSerializer(serializers.ModelSerializer):
    walk_trail = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    feedback_image_url = serializers.SerializerMethodField()
    response_image_url = serializers.SerializerMethodField()
    response_content = serializers.SerializerMethodField()

    class Meta:
        model = Response
        fields = [
            'walk_trail',
            'location',
            'feedback_image_url',
            'response_image_url',
            'response_content',
        ]

    def get_walk_trail(self, obj):
        return obj.feedback.walktrail.name if obj.feedback.walktrail else None
    
    def get_location(self, obj):
        return obj.feedback.location if obj.feedback.location else None

    def get_response_image_url(self, obj):
        return obj.response_image_url or None
        
    def get_feedback_image_url(self, obj):
        return obj.feedback.feedback_image_url or None
        
    def get_response_content(self, obj):
        return obj.response_content or "No response content provided"