from rest_framework import serializers
from .models import Response
from walktrails.models import WalkTrail,Route
from feedback.models import Feedback

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['id', 'category','latitude','longitude', 'created_at', 'updated_at']

class CurrentFeedbackSerializer(serializers.ModelSerializer):
    feedbacks = serializers.SerializerMethodField()

    class Meta:
        model = WalkTrail
        fields = ['name', 'feedbacks']
    
    def get_feedbacks(self, obj):
        feedbacks = Feedback.objects.filter(status='in_progress', walktrail=obj).order_by('-created_at')
        return FeedbackSerializer(feedbacks, many=True).data

class FeedbackSummarySerializer(serializers.ModelSerializer):
    suggestion_count = serializers.IntegerField()
    inconvenience_count = serializers.IntegerField()

    class Meta:
        model = WalkTrail
        fields = ['name', 'suggestion_count', 'inconvenience_count']

class FeedbackCategoryCountSerializer(serializers.Serializer):
    walktrail_name = serializers.CharField(source='walktrail__name')
    type = serializers.CharField()
    count_category1 = serializers.IntegerField()
    count_category2 = serializers.IntegerField()
    count_category3 = serializers.IntegerField()
    count_category4 = serializers.IntegerField()

    class Meta:
        model = Feedback
        fields = ['walktrail__name','type', 'count_category1', 'count_category2','count_category3','count_category4']

# Response List Serializer
class ResponseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response
        fields = [
            'id',
            'admin',
            'feedback',
            'status',
            'responded_at',
        ]
        read_only_fields = [
            'id',
            'feedback',
            'admin',
            'responded_at',
        ]


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
        walktrail = obj.feedback.walktrail
        return walktrail.name if walktrail else None
    
    def get_location(self, obj):
        return obj.feedback.location if obj.feedback else None

    def get_feedback_image_url(self, obj):
        feedback_image = obj.feedback.feedback_image_url
        return feedback_image if feedback_image else None

    def get_response_content(self, obj):
        return obj.response_content

    def get_response_image_url(self, obj):
        return obj.response_image_url if obj.response_image_url else None