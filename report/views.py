from django.shortcuts import render
from openai import OpenAI
from decouple import config

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
    You are a municipal official drafting an official report. Output a valid JSON object only (JSON).
    Style: formal, {style}
    [출력 규칙]
    현재 보고서의 제목은 {title}이고(출력값에서는 제외), 
    {section}를 key로 해서 json 형식으로 작성해줘
    """
    CONTENT ="""
    [작성 지시] {instruction}
    [참고자료] {docs}
    """
    system = SYSTEM.format(title=title, section=section, style=style)
    content = CONTENT.format( instruction=instruction, docs=docs)
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

result = create_ai_report(
    title="배봉산·현장상·정릉천·중랑천 둘레길 연계 명품 산책로 신설",
    section="1-11 추진배경/사업개요",
    instruction=(
        "추진배경: 야간 도시경관 개선, 배봉산 지역명소화, 구 상징성 강화를 중심으로 요약.\n"
        "사업개요: 위치, 기간(2023~2026), 총사업비, 추진부서, 시행방식, 세부사업 구성 3~5개.\n"
        "추진일정: 연도별 주요 마일스톤 간단 항목화.\n"
        "재원: 항목/금액/비고 2~4개.\n"
        "기대효과·홍보방안: 항목형 3~5개."
    ),
    style="formal, terse, itemized",
    docs="""
- 기본자료: 도시경관 개선(야간), 배봉산 지역명소화, '꽃의 도시·탄소중립도시' 미래 지향.
- 기간: 2023~2026, 단계적 추진. 총사업비 25억 원(예시).
- 위치: 배봉산 일대 및 둘레길 연계.
- 세부: 조명경관 연출, 벽면 경관개선, 안전시설 보강, 안내체계 개선, 휴게시설 정비.
- 홍보: 지역축제 연계, SNS 콘텐츠, 야간경관 체험행사.
"""
)
print(result)