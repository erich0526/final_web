from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'NBA'

urlpatterns = [
    path('', views.home, name='home'),
    path('schedule/', views.schedule, name='schedule'),
    path('boxscore/<int:game_id>/', views.game_detail, name='game_detail'),
    path('add_comment/<int:game_id>/', views.add_comment, name='add_comment'),
    path('toggle_pin_comment/<int:comment_id>/', views.toggle_pin_comment, name='toggle_pin_comment'),
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('login/', auth_views.LoginView.as_view(
        template_name='NBA/login.html',
        redirect_authenticated_user=True,
        next_page='NBA:home'
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='NBA:home'), name='logout'),
    path('register/', views.register_view, name='register'),
] 