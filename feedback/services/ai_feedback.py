import openai
from decouple import config
from django.conf import settings
from feedback.models import Feedback
import json
from django.db import transaction

# 재준이형꺼
def run_ai_analysis(content):
    system ="""
    당신은 산책로 민원 데이터를 처리하는 공무원입니다.
    아래 “민원 원문”을 분석하여, 지정된 JSON 스키마에 맞춰 결과만 반환하세요.
    반드시 유효한 JSON만 출력하세요. 불필요한 텍스트는 출력하지 마세요.
    
    [제약]
    - ai_keyword: 한 단어만.
    - ai_situation: 문제 상황을 적어주고, 없으면 null로
    - ai_demand: 요구사항을 적어주고, 없으면 null로
    - ai_importance: "높음" | "중간" | "낮음" (높음: 안전 관련 / 중간: 불편하지만 긴급하진 않음 / 낮음: 개선되면 좋지만 시급하지 않음)
    - ai_expected_duration: "단기" | "중장기".
    - ai_note: 그 외 특이사항, 없으면 null
    }
    """
    openai.api_key = settings.OPENAI_API_KEY
    resp = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        temperature=0.1,
        response_format={"type": "json_object"},
        messages=[
        {"role": "system", "content": system},
        {"role": "user", "content": content},
        ],
    )
    return resp

def apply_ai_analysis_to_feedbacks():
    feedbacks = Feedback.objects.all()

    for feedback in feedbacks:
        try:
            # AI 분석 실행
            ai_response = run_ai_analysis(feedback.feedback_content)
            ai_result = json.loads(ai_response.choices[0].message.content)

            # 필드 적용
            feedback.ai_keyword = ai_result.get("ai_keyword")
            feedback.ai_situation = ai_result.get("ai_situation")
            feedback.ai_demand = ai_result.get("ai_demand")
            feedback.ai_importance = ai_result.get("ai_importance")
            feedback.ai_expected_duration = ai_result.get("ai_expected_duration")
            feedback.ai_note = ai_result.get("ai_note")

            feedback.save()
            print(f"Feedback {feedback.id} updated successfully.")

        except json.JSONDecodeError:
            print(f"Feedback {feedback.id} - JSON 파싱 오류 발생")
        except Exception as e:
            print(f"Feedback {feedback.id} - 예외 발생: {e}")