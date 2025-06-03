from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json
from .models import Game, Player, Comment
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST

def home(request):
    games = Game.objects.all().order_by('-date')[:10]
    return render(request, 'NBA/home.html', {'games': games})

def game_detail(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    home_players = Player.objects.filter(game=game, team=game.home_team)
    away_players = Player.objects.filter(game=game, team=game.away_team)
    comments = Comment.objects.filter(game=game).order_by('-is_pinned', '-created_at')
    
    return render(request, 'NBA/game_detail.html', {
        'game': game,
        'home_players': home_players,
        'away_players': away_players,
        'comments': comments
    })

@login_required
@csrf_exempt
def add_comment(request, game_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            game = get_object_or_404(Game, id=game_id)
            
            comment = Comment.objects.create(
                game=game,
                author=request.user.username,
                content=data['content']
            )
            
            return JsonResponse({
                'success': True,
                'author': comment.author,
                'content': comment.content,
                'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S')
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@user_passes_test(lambda u: u.is_staff)
@csrf_exempt
def toggle_pin_comment(request, comment_id):
    if request.method == 'POST':
        try:
            comment = get_object_or_404(Comment, id=comment_id)
            comment.is_pinned = not comment.is_pinned
            comment.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@user_passes_test(lambda u: u.is_staff)
@csrf_exempt
def delete_comment(request, comment_id):
    if request.method == 'POST':
        try:
            comment = get_object_or_404(Comment, id=comment_id)
            comment.delete()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def schedule(request):
    games = Game.objects.filter(date__gte=timezone.now()).order_by('date')
    return render(request, 'NBA/schedule.html', {'games': games})
