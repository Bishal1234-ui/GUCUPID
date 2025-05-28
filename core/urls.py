from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('auth/', views.auth_view, name='auth'),
    path('logout/', views.logout_view, name='logout'),
    path('profile-setup/', views.profile_setup, name='profile_setup'),
    path('like/', views.like_profile, name='like_profile'),
    path('chat/<int:match_id>/', views.chat, name='chat'),
    path('send-message/<int:match_id>/', views.send_message, name='send_message'),
    path('get-messages/<int:match_id>/', views.get_messages, name='get_messages'),
    path('unmatch/', views.unmatch_user, name='unmatch_user'),
    path('reset-rejected/', views.reset_rejected_profiles, name='reset_rejected_profiles'),
]