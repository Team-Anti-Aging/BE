# walktrails/serializers.py

from rest_framework import serializers
from .models import WalkTrail, Route

class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ['name', 'latitude', 'longitude']

class SimpleRouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ['name']
class WalkTrailSerializer(serializers.ModelSerializer):
    # 산책로 정보(리스트 나열용)
    class Meta:
        model = WalkTrail
        fields = ['name', 'duration', 'distance_km']

class WalkTrailInfoSerializer(serializers.ModelSerializer):
    # 산책로 선택 페이지(정보)
    routes = serializers.SerializerMethodField()

    class Meta:
        model = WalkTrail
        fields = ['name', 'duration', 'distance_km', 'description', 'routes']

    def get_routes(self, obj):
        queryset = obj.routes.all().order_by('order')
        filtered = queryset[0::5]  # 0부터 5개씩 띄엄띄엄
        return SimpleRouteSerializer(filtered, many=True).data
    
class WalkTrailRouteSerializer(serializers.ModelSerializer):
    # 산책로 루트 출력
    routes = RouteSerializer(many = True)
    
    class Meta:
        model = WalkTrail
        fields = ['name', 'routes']