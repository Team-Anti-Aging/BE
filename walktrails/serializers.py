# walktrails/serializers.py

from rest_framework import serializers
from .models import WalkTrail, Route

# route 테이블 관련
class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ['latitude', 'longitude']

# walktrail 테이블 관련
class WalkTrailListSerializer(serializers.ModelSerializer):
    # 산책로 리스트
    class Meta:
        model = WalkTrail
        fields = ['name', 'duration', 'distance_km']

class WalkTrailInfoSerializer(serializers.ModelSerializer):
    routes = RouteSerializer(many = True)
    # 특정 산책로 정보 조회
    class Meta:
        model = WalkTrail
        fields = ['name', 'duration', 'distance_km', 'description', 'checkpoint', 'routes']

class WalkTrailRouteSerializer(serializers.ModelSerializer):
    # 산책로 루트 출력
    routes = RouteSerializer(many = True)
    
    class Meta:
        model = WalkTrail
        fields = ['name', 'routes']