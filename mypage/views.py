from django.shortcuts import render
from rest_framework import generics, permissions
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count, Q

from .models import Favorite_walktrail
from .serializers import FavoriteSerializer
from walktrails.models import WalkTrail
from walktrails.serializers import WalkTrailListSerializer
from feedback.models import Feedback
from feedback.serializers import FeedbackSerializer

# Create your views here.
class Mypage_view(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        feedback_count = Feedback.objects.filter(user=user).count()
        favorite_count = Favorite_walktrail.objects.filter(user=user).count()

        return Response({
            "feedback_count": feedback_count,
            "favorite_count": favorite_count,
        })
    
class Favorite_walktrail_view(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        walktrail_name = kwargs.get("walktrail_name")
        walktrail = get_object_or_404(WalkTrail, name=walktrail_name)
        serializer = FavoriteSerializer(data={})
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, walktrail = walktrail)
            return Response(status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, *args, **kwargs):
        walktrail_name = kwargs.get("walktrail_name")
        walktrail = get_object_or_404(WalkTrail, name=walktrail_name)
        favorite = get_object_or_404(Favorite_walktrail, user = request.user, walktrail = walktrail)
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class Favorite_walktrail_list_view(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = WalkTrailListSerializer
    pagination_class = None
    
    def get_queryset(self):
        return WalkTrail.objects.filter(
            id__in=Favorite_walktrail.objects.filter(user=self.request.user).values_list('walktrail', flat=True)
        )
    
class Feedback_list_view(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FeedbackSerializer
    pagination_class = None

    def get_queryset(self):
        user = self.request.user
        return Feedback.objects.filter(user=user)