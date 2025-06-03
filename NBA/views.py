from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
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
def add_comment(request, game_id):
    if request.method == 'POST':
        game = get_object_or_404(Game, id=game_id)
        content = request.POST.get('content')
        
        if content:
            comment = Comment.objects.create(
                game=game,
                author=request.user.username,
                content=content
            )
            # 添加成功後，重新導向回比賽詳細頁面
            return redirect('NBA:game_detail', game_id=game.id)
        else:
             # 如果內容為空，導向回頁面並可能顯示錯誤訊息
             messages.error(request, "留言內容不能為空。")
             return redirect('NBA:game_detail', game_id=game.id)

    # 非 POST 請求導向回比賽詳細頁面
    return redirect('NBA:game_detail', game_id=game_id)

@user_passes_test(lambda u: u.is_staff)
def toggle_pin_comment(request, comment_id):
    if request.method == 'POST':
        try:
            comment = get_object_or_404(Comment, id=comment_id)
            comment.is_pinned = not comment.is_pinned
            comment.save()
            # 固定/取消固定成功後，重新導向回比賽詳細頁面
            return redirect('NBA:game_detail', game_id=comment.game.id)
        except Exception as e:
             # 處理錯誤並導向回頁面
             messages.error(request, f"固定/取消固定留言失敗：{str(e)}")
             return redirect('NBA:game_detail', game_id=comment.game.id)
             
    # 非 POST 請求導向回首頁或比賽詳細頁，這裡暫時導向首頁
    return redirect('NBA:home')

@user_passes_test(lambda u: u.is_staff)
def delete_comment(request, comment_id):
    if request.method == 'POST':
        try:
            comment = get_object_or_404(Comment, id=comment_id)
            game_id = comment.game.id # 獲取留言所屬的比賽 ID
            comment.delete()
            # 刪除成功後，重新導向回比賽詳細頁面
            return redirect('NBA:game_detail', game_id=game_id)
        except Exception as e:
            # 刪除失敗並導向回頁面
            messages.error(request, f"刪除留言失敗：{str(e)}")
            return redirect('NBA:game_detail', game_id=comment.game.id)
             
    # 非 POST 請求也導向回首頁或比賽詳細頁，這裡暫時導向首頁
    return redirect('NBA:home')

def schedule(request):
    games = Game.objects.filter(date__gte=timezone.now()).order_by('date')
    return render(request, 'NBA/schedule.html', {'games': games})

# 新增修改留言視圖
@login_required
def edit_comment_view(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    # 檢查是否為留言作者
    if request.user.username != comment.author:
        messages.error(request, "您沒有權限修改這則留言。")
        return redirect('NBA:game_detail', game_id=comment.game.id)

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            comment.content = content
            comment.save()
            messages.success(request, "留言已成功修改。")
            return redirect('NBA:game_detail', game_id=comment.game.id)
        else:
            messages.error(request, "留言內容不能為空。")
    
    # GET 請求或 POST 內容為空時，顯示修改表單
    return render(request, 'NBA/edit_comment.html', {'comment': comment})

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        # 驗證密碼是否匹配
        if password1 != password2:
            messages.error(request, '兩次輸入的密碼不相符')
            return render(request, 'NBA/login.html', {'error_message': '兩次輸入的密碼不相符', 'show_register': True})
        
        # 檢查使用者名稱是否已存在
        if User.objects.filter(username=username).exists():
            messages.error(request, '使用者名稱已被使用')
            return render(request, 'NBA/login.html', {'error_message': '使用者名稱已被使用', 'show_register': True})
        
        # 檢查電子郵件是否已存在
        if User.objects.filter(email=email).exists():
            messages.error(request, '電子郵件已被註冊')
            return render(request, 'NBA/login.html', {'error_message': '電子郵件已被註冊', 'show_register': True})
        
        # 創建新用戶
        try:
            user = User.objects.create_user(username=username, email=email, password=password1)
            login(request, authenticate(username=username, password=password1))
            messages.success(request, f'成功註冊並登入！ 歡迎, {username}!')
            return redirect('NBA:home')
        except Exception as e:
            messages.error(request, f'註冊失敗：{str(e)}')
            return render(request, 'NBA/login.html', {'error_message': f'註冊失敗：{str(e)}', 'show_register': True})
    
    return redirect('NBA:login')

def login_view(request):
    # 這個 view 是由 django.contrib.auth.views.LoginView 處理的
    # 這裡只是為了有個名稱可以 redirect 到
    pass
