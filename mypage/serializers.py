from rest_framework import serializers
from .models import Favorite_walktrail
from walktrails.models import WalkTrail

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite_walktrail
        fields = ["id", "user", "walktrail", "created_at"]
        read_only_fields = ["id", "user", "walktrail", "created_at"]