import boto3
import openai
from uuid import uuid4
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from .models import *
from .models import Response as ResponseModel
from .serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView
from feedback.models import Feedback, WalkTrail
from django.db.models import Count, Q, F
from django.utils.timezone import now
from feedback.serializers import OnlyFeedbackSerializer

# 각 산책로별 피드백 현황
class FeedbackinProgress(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        qs = WalkTrail.objects.annotate(
            unresolved_count=Count('feedback', filter=Q(feedback__status='in_progress')),            
        ).values('name', 'unresolved_count')
        return Response(list(qs))
    
# 각 산책로별 피드백 리스트 (상위 5개)
class CurrentFeedbackList(generics.ListAPIView):
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        walktrail_name = self.kwargs.get('walktrail_name')
        qs = Feedback.objects.filter(
            walktrail__name=walktrail_name,
        ).order_by('-created_at')[:5]
        return qs

# 산책로 현황 기본 화면
class EntireFeedbackView(generics.ListAPIView):
    serializer_class = FeedbackSummarySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WalkTrail.objects.values('name').annotate(
            suggestion_count=Count('feedback', filter=Q(feedback__type='제안')),
            inconvenience_count=Count('feedback', filter=Q(feedback__type='불편'))
        ).order_by('id')

#산책로별 상세 현황
class FeedbackByTrailView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FeedbackCategoryCountSerializer

    def get(self, request, walktrail_name):
        qs = Feedback.objects.filter(walktrail__name=walktrail_name).values(
            'walktrail__name', 'type'
        ).annotate(
            count_category1=Count(
                'id',
                filter=Q(type='불편', category='안전') | Q(type='제안', category='편의시설 확충')
            ),
            count_category2=Count(
                'id',
                filter=Q(type='불편', category='청결') | Q(type='제안', category='경관 개선')
            ),
            count_category3=Count(
                'id',
                filter=Q(type='불편', category='이동성') | Q(type='제안', category='정보 제공')
            ),
            count_category4=Count(
                'id',
                filter=Q(type='불편', category='소음방해') | Q(type='제안', category='프로그램/이벤트')
            )


        ).order_by('walktrail__name','type')

        return Response(FeedbackCategoryCountSerializer(qs, many=True).data)

# 금일 신고 내역 (산책로 별 / (불편, 제안) 별)
# ==============================================================================================
class TodayFeedbackView(generics.ListAPIView):
    serializer_class = CurrentFeedbackSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        today = now().date()
        return WalkTrail.objects.annotate(
            suggestion_count=Count(
                'feedback',
                filter=Q(feedback__type='제안', feedback__created_at__date=today)
            ),
            inconvenience_count=Count(
                'feedback',
                filter=Q(feedback__type='불편', feedback__created_at__date=today)
            )
        ).order_by('name')

# 특정 산책로의 최근 피드백
class RecentFeedbackView(generics.ListAPIView):
    serializer_class = OnlyFeedbackSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        today = now().date()
        walktrail_name = self.kwargs.get('walktrail_name')
        pk = self.kwargs.get('pk')  # 선택적으로 들어올 수 있음
        qs = Feedback.objects.filter(walktrail__name=walktrail_name, created_at__date=today, status='in_progress')

        if pk is not None:
            qs = qs.filter(pk=pk)  # 특정 feedback 하나만
        else:
            qs = qs.order_by('-created_at')  # 리스트일 경우 최신순

        return qs
    
# ============================================================================================================
# 피드백에 대한 응답 생성 뷰
# 응답생성 시 자동 status 값 조정 로직 개선
class ResponseCreateView(generics.CreateAPIView):
    queryset = ResponseModel.objects.all()
    serializer_class = ResponseCreateSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        feedback = Feedback.objects.get(pk=pk)

        image_url = None

        image = self.request.FILES.get('response_image')

        if image:
            s3 = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_S3_REGION_NAME,
            )
            bucket_name = settings.AWS_STORAGE_BUCKET_NAME
            ext = image.name.split('.')[-1]
            file_key = f"response_images/{uuid4()}.{ext}"

            s3.upload_fileobj(
                image,
                bucket_name,
                file_key,
                ExtraArgs={'ContentType': image.content_type}
            )

            image_url = f"https://{bucket_name}.s3.amazonaws.com/{file_key}"
        
        serializer.save(
            admin=self.request.user,
            feedback=feedback,
            response_image_url=image_url
        )

        feedback.status = 'completed'
        feedback.save()
    

class RespondedFeedbackView(generics.ListAPIView):
    serializer_class = RespondedFeedbackSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        walktrail_name = self.kwargs.get('walktrail_name')
        return ResponseModel.objects.filter(
            feedback__walktrail__name=walktrail_name,
            feedback__status='completed'
        ).order_by('-responded_at')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)  # DRF 응답 객체로 반환

class MonthlyStatsView(APIView):
    # permission_classes = [permissions.IsAdminUser]
    permission_classes = [permissions.AllowAny]

    def post(self, request, walktrail_name):
        walktrail = get_object_or_404(WalkTrail, name=walktrail_name)
        year = request.data.get('year')
        month = request.data.get('month')

        if not year or not month:
            year, month = now().year, now().month
        
        qs = Feedback.objects.filter(
            walktrail=walktrail,
            created_at__year=year,
            created_at__month=month
        )

        total_feedbacks = qs.count()

        type_counts = qs.values('type').annotate(count=Count('id'))
        type_dict = {item['type']: item['count'] for item in type_counts}
        type_ratios = {
            type: round((cnt/total_feedbacks)*100, 1) if total_feedbacks > 0 else 0
            for type, cnt in type_dict.items()
        }

        category_counts = qs.values('category').annotate(count=Count('id'))
        category_dict = {item["category"]: item["count"] for item in category_counts}

        category_ratios = {
            category: round((cnt/total_feedbacks)*100, 1) if total_feedbacks > 0 else 0
            for category, cnt in category_dict.items()
        }

        completed_counts = qs.filter(status='completed').count()

        status_counts = {
            "처리 완료": completed_counts,
            "진행 중": qs.filter(status='in_progress').count()
        }

        stats, created = Monthly_ReportStats.objects.update_or_create(
            walktrail=walktrail,
            year=year,
            month=month,
            defaults={
                "total_feedbacks": total_feedbacks,
                "type_counts": type_dict,
                "type_ratios": type_ratios,
                "category_counts": category_dict,
                "category_ratios": category_ratios,
                "completed_counts": completed_counts,
                "status_counts": status_counts,
            }
        )

        return Response({
            status.HTTP_200_OK if created else status.HTTP_200_OK: "Created" if created else "Updated",
        })




class AIReportOpenAIView(APIView):
    def post(self, request, walktrail_name):
        # 산책로 객체 가져오기
        try:
            walktrail = WalkTrail.objects.get(name=walktrail_name)
        except WalkTrail.DoesNotExist:
            return Response({"error": "해당 산책로가 존재하지 않습니다."}, status=404)

        # 월과 연도 가져오기
        year = request.data.get('year')
        month = request.data.get('month')

        # Feedback 조회
        feedbacks = Feedback.objects.filter(walktrail=walktrail, ai_importance="높음",created_at__year=year, created_at__month=month)
        if not feedbacks.exists():
            return Response({"message": "해당 산책로 피드백이 없습니다."})

        monthlyreport = Monthly_ReportStats.objects.filter(walktrail=walktrail, year=year, month=month).first()
        if not monthlyreport:
            return Response({"message": "해당 산책로 월간 통계가 없습니다."})

        # 프롬프트 생성
        feedback_texts = "\n".join(
            f"- [{f.type}] {f.category} / {f.location}: {f.feedback_content}"
            for f in feedbacks
        )

        monthlyreport_texts = f"""
        - 산책로명: {walktrail.name}
        - 연도: {monthlyreport.year}
        - 월: {monthlyreport.month}
        - 산책로 피드백 건수 계: {monthlyreport.total_feedbacks}
        - 피드백 유형별 건수: {monthlyreport.type_counts}
        - 피드백 유형별 비율 (단위: %): {monthlyreport.type_ratios}
        - 피드백 카테고리별 건수: {monthlyreport.category_counts}
        - 피드백 카테고리별 비율 (단위: %): {monthlyreport.category_ratios}
        - 완료된 피드백 건수: {monthlyreport.completed_counts}
        - 상태별 피드백 건수: {monthlyreport.status_counts}
        """

        prompt = f"""
        당신은 동대문구 산책로 개선사업 담당 관리자입니다.
        아래 피드백 데이터를 분석해서 종합 리포트를 작성해주세요.
        피드백 데이터:
        {feedback_texts}
        월간 통계 데이터:
        {monthlyreport_texts}

        보고서 양식:
        1. 기본 현황 (DB 기반)
        - 산책로 이름
        - 전체 민원 수
        - 불편/제안 비율
        - 카테고리별 비중

        2. 분석 및 특이사항 (AI 기반)
        - 주요 민원 유형
        - 데이터에서 확인되는 특이사항, 이상치, 주목할 만한 패턴

        3. 우선순위 및 처리 소요 (ai_expected_duration 값에 따른 분류)
        - 긴급 처리 항목 (즉시 대응 필요): ai_expected_duration 필드값이 "긴급"인 항목
        - 단기 처리 가능 항목 (이번 달 내 해결 가능): ai_expected_duration 필드값이 "단기"인 항목
        - 중장기 개선 필요 항목 (추후 계획 수립 필요): ai_expected_duration 필드값이 "중장기"인 항목

        4. 결론 및 제안 (AI 기반)
        - 이번 달 핵심 과제 요약: ai_expected_duration 필드값이 긴급 내지는 단기인 항목을 우선적으로 반영하여 리스트 형태로 반환할 것
        - 다음 달 대응 방향 제안: feedback 데이터의 내용을 총체적으로 고려하여 문제 해결 방법의 사례를 첨언하여 리스트 형태로 반환할 것.

        조건:
        - 한국어로 작성
        - 각 항목별 소제목 명확히 표시
        - 글머리표와 번호를 적절히 활용하여 가독성 높이기
        - 필드의 데이터값을 임의로 적용 금지, 반드시 적힌 내용대로만 분류
        - 데이터에서 확인 가능한 내용만 활용, 추가 설명 금지
        - 문장은 간결하고 실무 회의용으로 체계적 작성

        이 보고서에 포함되지 않은 다른 텍스트나 불필요한 서술은 작성하지 마세요.
        """

        # OpenAI 최신 API 호출
        openai.api_key = settings.OPENAI_API_KEY
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "당신은 데이터 분석 전문가입니다."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000,
        )

        report_text = response.choices[0].message.content

        # DB 저장
        ai_report, _ = AIReport.objects.update_or_create(
            walktrail=walktrail,
            defaults={"report_text": report_text}
        )

        print(report_text)

        # 프론트 반환
        return Response({
            "walktrail_name": walktrail.name,
            "ai_report": report_text
        })