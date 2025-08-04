from rest_framework import serializers
from .models import Response

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