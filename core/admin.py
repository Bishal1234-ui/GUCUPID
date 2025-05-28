from django.contrib import admin
from .models import Profile, Like, Match, Message


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'age', 'gender', 'created_at')
    list_filter = ('gender', 'age', 'created_at')
    search_fields = ('name', 'user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user', 'is_like', 'created_at')
    list_filter = ('is_like', 'created_at')
    search_fields = ('from_user__username', 'to_user__username')


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('user1', 'user2', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user1__username', 'user2__username')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'match', 'content_preview', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('sender__username', 'content')
    
    def content_preview(self, obj):
        return obj.content[:50] + ('...' if len(obj.content) > 50 else '')
    content_preview.short_description = 'Content'