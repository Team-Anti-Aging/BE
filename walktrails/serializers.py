# walktrails/serializers.py

from rest_framework import serializers
from .models import WalkTrail, Route

class WalkTrailListSerializer(serializers.ModelSerializer):
    # 산책로 리스트
    class Meta:
        model = WalkTrail
        fields = ['name', 'duration', 'distance_km']

class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ['lat', 'lng']

class WalkTrailRouteSerializer(serializers.ModelSerializer):
    routes = RouteSerializer(many = True)

    class Meta:
        model = WalkTrail
        fields = ['name', 'routes']  

class WalkTrailInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalkTrail
        fields = ['name', 'duration', 'distance_km', 'description', 'checkpoint']

class WalkTrailRouteSerializer(serializers.ModelSerializer):
    # 산책로 루트 출력
    routes = RouteSerializer(many = True)
    
    class Meta:
        model = WalkTrail
        fields = ['name', 'routes']