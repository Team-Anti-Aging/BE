# walktrails/serializers.py

from rest_framework import serializers
from .models import WalkTrail, Route
from mypage.models import Favorite_walktrail

class WalkTrailListSerializer(serializers.ModelSerializer):
    is_favorited = serializers.SerializerMethodField()
    # 산책로 리스트
    class Meta:
        model = WalkTrail
        fields = ['name', 'duration', 'distance_km', 'is_favorited']

    def get_is_favorited(self,obj):
        request = self.context.get("request")
        user = getattr(request, "user", None)

        if not user or not user.is_authenticated:
            return False
        
        return Favorite_walktrail.objects.filter(user=user, walktrail=obj).exists()

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