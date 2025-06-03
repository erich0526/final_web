from django.core.management.base import BaseCommand
from django.utils import timezone
from NBA.models import Game, Player
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = '加載示例比賽數據'

    def handle(self, *args, **kwargs):
        # 創建比賽
        game1 = Game.objects.create(
            home_team='洛杉磯湖人',
            away_team='金州勇士',
            home_score=108,
            away_score=112,
            date=timezone.now() - timedelta(hours=2),
            status='已結束'
        )

        # 湖人隊球員
        Player.objects.create(
            game=game1,
            name='LeBron James',
            team='洛杉磯湖人',
            points=28,
            assists=8,
            rebounds=12,
            steals=2,
            blocks=1,
            minutes_played='36:24'
        )
        Player.objects.create(
            game=game1,
            name='Anthony Davis',
            team='洛杉磯湖人',
            points=24,
            assists=3,
            rebounds=15,
            steals=1,
            blocks=3,
            minutes_played='34:18'
        )

        # 勇士隊球員
        Player.objects.create(
            game=game1,
            name='Stephen Curry',
            team='金州勇士',
            points=32,
            assists=7,
            rebounds=5,
            steals=2,
            blocks=0,
            minutes_played='38:15'
        )
        Player.objects.create(
            game=game1,
            name='Klay Thompson',
            team='金州勇士',
            points=26,
            assists=3,
            rebounds=6,
            steals=1,
            blocks=1,
            minutes_played='35:42'
        )

        # 第二場比賽
        game2 = Game.objects.create(
            home_team='波士頓塞爾提克',
            away_team='邁阿密熱火',
            home_score=124,
            away_score=118,
            date=timezone.now() - timedelta(hours=1),
            status='已結束'
        )

        # 塞爾提克球員
        Player.objects.create(
            game=game2,
            name='Jayson Tatum',
            team='波士頓塞爾提克',
            points=35,
            assists=5,
            rebounds=8,
            steals=2,
            blocks=1,
            minutes_played='38:45'
        )
        Player.objects.create(
            game=game2,
            name='Jaylen Brown',
            team='波士頓塞爾提克',
            points=28,
            assists=4,
            rebounds=7,
            steals=1,
            blocks=0,
            minutes_played='36:20'
        )

        # 熱火球員
        Player.objects.create(
            game=game2,
            name='Jimmy Butler',
            team='邁阿密熱火',
            points=30,
            assists=6,
            rebounds=9,
            steals=3,
            blocks=1,
            minutes_played='39:15'
        )
        Player.objects.create(
            game=game2,
            name='Bam Adebayo',
            team='邁阿密熱火',
            points=22,
            assists=4,
            rebounds=12,
            steals=1,
            blocks=2,
            minutes_played='35:30'
        )

        # 第三場比賽
        game3 = Game.objects.create(
            home_team='達拉斯小牛',
            away_team='鳳凰城太陽',
            home_score=95,
            away_score=89,
            date=timezone.now(),
            status='進行中'
        )

        # 小牛球員
        Player.objects.create(
            game=game3,
            name='Luka Doncic',
            team='達拉斯小牛',
            points=32,
            assists=8,
            rebounds=7,
            steals=2,
            blocks=0,
            minutes_played='32:15'
        )
        Player.objects.create(
            game=game3,
            name='Kyrie Irving',
            team='達拉斯小牛',
            points=25,
            assists=6,
            rebounds=4,
            steals=1,
            blocks=0,
            minutes_played='30:45'
        )

        # 太陽球員
        Player.objects.create(
            game=game3,
            name='Devin Booker',
            team='鳳凰城太陽',
            points=28,
            assists=5,
            rebounds=6,
            steals=1,
            blocks=0,
            minutes_played='33:20'
        )
        Player.objects.create(
            game=game3,
            name='Kevin Durant',
            team='鳳凰城太陽',
            points=24,
            assists=4,
            rebounds=8,
            steals=2,
            blocks=1,
            minutes_played='31:15'
        )

        self.stdout.write(self.style.SUCCESS('成功加載示例數據！')) 