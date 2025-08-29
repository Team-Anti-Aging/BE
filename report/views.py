from django.shortcuts import render
from openai import OpenAI
from decouple import config
from rest_framework import generics, permissions
from rest_framework import status
from rest_framework.response import Response
from feedback.models import Feedback
from .serializers import ReportSerializer


# Create your views here.
def ai_monthly_report():
    system ="""
    """
    content ="""
    """
    api_key = config("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.1,
        response_format={"type": "json_object"},
        messages=[
        {"role": "system", "content": system},
        {"role": "user", "content": content},
        ],
    )
    return resp

def create_ai_report(title, section, style, instruction, docs):
    SYSTEM ="""
    You are a municipal official drafting an official report. 
    Style: formal, {style}
    [출력 규칙]
    현재 보고서의 제목은 {title}이고(출력값에서는 제외), 
    {section}를 기준으로 항목을 나눠서 작성해줘
    """
    CONTENT ="""
    [작성 지시] {instruction}
    [참고자료] {docs}
    """
    system = SYSTEM.format(title=title, section=section, style=style)
    content = CONTENT.format(instruction=instruction, docs=docs)
    api_key = config("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.1,
        messages=[
        {"role": "system", "content": system},
        {"role": "user", "content": content},
        ],
    )
    return resp



class Custom_AI_report_view(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ReportSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = ReportSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        report_info = serializer.save()
        title = report_info.title
        section = report_info.section
        style = report_info.style
        instruction = report_info.instruction

        docs_ids = list(report_info.docs_id.values_list("id", flat=True))
        docs = Feedback.objects.filter(id__in=docs_ids).values(
            "walktrail__name", "location", "type", "category", "feedback_image_url",
            "ai_keyword","ai_situation","ai_demand","ai_importance","ai_expected_duration" 
        )

        if not docs.exists():
            return Response({"detail": "유효한 docs가 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

        ai_report = create_ai_report(title, section, style, instruction, docs)
        report = ai_report.choices[0].message.content
        serializer.save(report=report)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
