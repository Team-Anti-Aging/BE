from rest_framework import serializers
from .models import Response

class ResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response
        fields = [
            'admin',
            # 'feedback',
            'status',
            'response_content',
            'responded_at',
            'response_image',
        ]
        read_only_fields = [
            'id',
            'responded_at',
        ]
