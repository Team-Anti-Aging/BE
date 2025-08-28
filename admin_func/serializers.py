from rest_framework import serializers
from .models import Response, AIReport, Monthly_ReportStats
from walktrails.models import WalkTrail,Route
from feedback.models import Feedback

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['id', 'category', 'type', 'latitude','longitude', 'created_at', 'updated_at']

class CurrentFeedbackSerializer(serializers.ModelSerializer):
    suggestion_count = serializers.IntegerField(read_only=True)
    inconvenience_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = WalkTrail
        fields = ['name', 'suggestion_count', 'inconvenience_count']

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
    response_image = serializers.ImageField(write_only=True, required=False) # 입력 전용
    
    class Meta:
        model = Response
        fields = ['response_content', 'response_image']


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

class MonthlyReportStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Monthly_ReportStats
        fields = '__all__'


class AIReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIReport
        fields = ['walktrail_name', 'report_text', 'created_at']