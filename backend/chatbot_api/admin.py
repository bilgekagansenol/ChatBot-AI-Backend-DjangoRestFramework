
from django.contrib import admin
from .models import ChatSession, ChatMessage

@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'created_on', 'last_uploaded')
    list_filter = ('user',)
    search_fields = ('title',)

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'session', 'is_user', 'timestamp')
    list_filter = ('session', 'is_user')
    search_fields = ('message',)
