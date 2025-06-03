from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Game(models.Model):
    home_team = models.CharField(max_length=100)
    away_team = models.CharField(max_length=100)
    home_score = models.IntegerField(null=True, blank=True)
    away_score = models.IntegerField(null=True, blank=True)
    date = models.DateTimeField()
    status = models.CharField(max_length=20)  # 進行中、已結束等
    venue = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.home_team} vs {self.away_team}"

class Player(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='players')
    name = models.CharField(max_length=100)
    team = models.CharField(max_length=100)
    points = models.IntegerField()
    assists = models.IntegerField()
    rebounds = models.IntegerField()
    steals = models.IntegerField()
    blocks = models.IntegerField()
    minutes_played = models.CharField(max_length=10)  # 格式：MM:SS

    def __str__(self):
        return f"{self.name} - {self.team}"

class Comment(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    is_pinned = models.BooleanField(default=False)  # 新增欄位，用於釘選留言

    def __str__(self):
        return f"{self.author} - {self.created_at}"
