from django.contrib import admin
from .models import Game, Player, Comment

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('home_team', 'away_team', 'home_score', 'away_score', 'date', 'status')
    list_filter = ('status', 'date')
    search_fields = ('home_team', 'away_team')

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'team', 'points', 'assists', 'rebounds', 'steals', 'blocks', 'minutes_played')
    list_filter = ('team',)
    search_fields = ('name',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'game', 'content', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('author', 'content')
