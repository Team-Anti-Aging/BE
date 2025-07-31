# walktrails/serializers.py

from rest_framework import serializers
from .models import WalkTrail, Route

class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ['id', 'trail', 'latitude', 'longitude']
        read_only_fields = ['id']

class WalkTrailSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalkTrail
        fields = ['id', 'name', 'time', 'distance', 'route_description', 'created_at']
        read_only_fields = ['id', 'created_at']

class WalkTrailDetailSerializer(serializers.ModelSerializer):
    routes = RouteSerializer(many=True, read_only=True)
    class Meta:
        model = WalkTrail
        fields = ['id', 'name', 'time', 'distance', 'route_description', 'created_at', 'routes']
        read_only_fields = ['id', 'created_at']