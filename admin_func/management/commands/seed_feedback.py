import json
from pathlib import Path
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from feedback.models import Feedback  # WalkTrail import 제거

User = get_user_model()


class Command(BaseCommand):
    help = "Load feedback data from JSON file (creates dummy users if missing)"

    def handle(self, *args, **options):
        path = Path("data/feedback_dummy.json")
        if not path.exists():
            self.stderr.write("❌ JSON 파일이 존재하지 않습니다.")
            return

        with open(path, "r", encoding="utf-8") as f:
            feedbacks = json.load(f)

        for feedback in feedbacks:
            # ✅ user 더미 생성/업데이트
            user_id = feedback["user"]
            User.objects.update_or_create(
                id=user_id,
                defaults={
                    "username": f"dummy_user_{user_id}",
                    "email": f"dummy_user_{user_id}@example.com",
                },
            )

            # ✅ feedback 저장
            Feedback.objects.update_or_create(
                id=feedback["id"],
                defaults={
                    "user_id": user_id,
                    "walktrail_id": feedback["walktrail"],  # 이미 존재한다고 하셨으니 그대로 사용
                    "location": feedback["location"],
                    "latitude": feedback["latitude"],
                    "longitude": feedback["longitude"],
                    "type": feedback["type"],
                    "category": feedback["category"],
                    "feedback_content": feedback["feedback_content"],
                    "feedback_image_url": feedback["feedback_image_url"],
                    "created_at": feedback["created_at"],
                    "updated_at": feedback["updated_at"],
                    "status": feedback["status"],
                },
            )
            self.stdout.write(f"✅ 피드백 '{feedback['id']}' 저장 완료")
        