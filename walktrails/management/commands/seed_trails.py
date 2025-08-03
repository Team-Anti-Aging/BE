# walk/management/commands/seed_trails.py

import json
from pathlib import Path
from django.core.management.base import BaseCommand
from walktrails.models import WalkTrail, Route

class Command(BaseCommand):
    help = '산책로와 경로 데이터를 JSON 파일로부터 시딩합니다.'

    def handle(self, *args, **options):
        path = Path('data/trail_data.json')
        if not path.exists():
            self.stderr.write("❌ JSON 파일이 존재하지 않습니다.")
            return

        with open(path, 'r', encoding='utf-8') as f:
            trails = json.load(f)

        for trail_data in trails:
            trail, _ = WalkTrail.objects.update_or_create(
                name=trail_data['name'],
                defaults={
                    'duration': trail_data['duration'],
                    'distance_km': trail_data['distance_km'],
                    'description': trail_data['description'],
                    'checkpoint' : trail_data['checkpoint']
                }
            )

            # 기존 경로 삭제 (중복 방지)
            trail.routes.all().delete()

            for i, route in enumerate(trail_data['routes']):
                Route.objects.create(
                    trail=trail,
                    latitude=route['lat'],
                    longitude=route['lng'],
                    order=i
                )

        self.stdout.write(self.style.SUCCESS("✅ 산책로 시딩이 완료되었습니다."))
