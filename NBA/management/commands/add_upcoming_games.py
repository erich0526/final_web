from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from NBA.models import Game

class Command(BaseCommand):
    help = '添加即將進行的比賽數據'

    def handle(self, *args, **kwargs):
        # 獲取當前時間
        now = timezone.now()
        
        # 定義一些即將進行的比賽
        upcoming_games = [
            {
                'home_team': 'Lakers',
                'away_team': 'Warriors',
                'date': now + timedelta(days=1),
                'venue': 'Crypto.com Arena',
                'home_score': None,
                'away_score': None
            },
            {
                'home_team': 'Celtics',
                'away_team': 'Bucks',
                'date': now + timedelta(days=2),
                'venue': 'TD Garden',
                'home_score': None,
                'away_score': None
            },
            {
                'home_team': 'Heat',
                'away_team': 'Nuggets',
                'date': now + timedelta(days=3),
                'venue': 'Miami-Dade Arena',
                'home_score': None,
                'away_score': None
            },
            {
                'home_team': 'Suns',
                'away_team': 'Mavericks',
                'date': now + timedelta(days=4),
                'venue': 'Footprint Center',
                'home_score': None,
                'away_score': None
            },
            {
                'home_team': 'Knicks',
                'away_team': '76ers',
                'date': now + timedelta(days=5),
                'venue': 'Madison Square Garden',
                'home_score': None,
                'away_score': None
            }
        ]

        # 添加比賽
        for game_data in upcoming_games:
            Game.objects.create(**game_data)
            self.stdout.write(
                self.style.SUCCESS(f'成功添加比賽: {game_data["home_team"]} vs {game_data["away_team"]}')
            ) 