from django.shortcuts import render
from django.db.models.query import QuerySet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics

from . import serializers
from . import models

# Create your views here.
class GetRouteAll(generics.ListAPIView):
    # 전체 산책로 좌표정보 받아오기 / 관리자용
    queryset = models.WalkTrail.objects.all()
    serializer_class = serializers.WalkTrailRouteSerializer
    pagination_class = None

class WalkTrail_list(generics.ListAPIView):
    # walktrail 리스트 조회
    queryset = models.WalkTrail.objects.all()
    serializer_class = serializers.WalkTrailListSerializer
    pagination_class = None

class WalkTrail_info(generics.RetrieveAPIView):
    # 특정 산책로 정보 조회
    queryset = models.WalkTrail.objects.all()
    serializer_class = serializers.WalkTrailInfoSerializer
    lookup_field = 'name'
    lookup_url_kwarg = 'name'


