from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json
from .models import Game, Player, Comment
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.contrib.auth import login, authenticate
from django.contrib import messages

def home(request):
    games = Game.objects.all().order_by('-date')[:10]
    now = timezone.now() # 獲取當前時間
    return render(request, 'NBA/home.html', {
        'games': games,
        'now': now, # 將當前時間傳給模板
    })

def game_detail(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    home_players = Player.objects.filter(game=game, team=game.home_team)
    away_players = Player.objects.filter(game=game, team=game.away_team)
    comments = Comment.objects.filter(game=game).order_by('-is_pinned', '-created_at')
    
    # 判斷比賽是否開始
    is_game_started = game.date <= timezone.now()
    
    return render(request, 'NBA/game_detail.html', {
        'game': game,
        'home_players': home_players,
        'away_players': away_players,
        'comments': comments,
        'is_game_started': is_game_started, # 將判斷結果傳給模板
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

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        # 驗證密碼是否匹配
        if password1 != password2:
            return render(request, 'NBA/login.html', {'error_message': '兩次輸入的密碼不相符', 'show_register': True})
        
        # 檢查使用者名稱是否已存在
        if User.objects.filter(username=username).exists():
            return render(request, 'NBA/login.html', {'error_message': '使用者名稱已被使用', 'show_register': True})
        
        # 檢查電子郵件是否已存在
        if User.objects.filter(email=email).exists():
            return render(request, 'NBA/login.html', {'error_message': '電子郵件已被註冊', 'show_register': True})
        
        # 創建新用戶
        try:
            user = User.objects.create_user(username=username, email=email, password=password1)
            login(request, authenticate(username=username, password=password1))
            return redirect('NBA:home')
        except Exception as e:
            return render(request, 'NBA/login.html', {'error_message': f'註冊失敗：{str(e)}', 'show_register': True})
    
    return redirect('NBA:login')
