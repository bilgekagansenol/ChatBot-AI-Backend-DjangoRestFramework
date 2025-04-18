from django.contrib import admin
from .models import PromptBoxItem, PromptBoxDialogue

class PromptBoxDialogueInline(admin.TabularInline):
    model = PromptBoxDialogue
    extra = 1

@admin.register(PromptBoxItem)
class PromptBoxItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'PromptBoxItem_information', 'user', 'created_on', 'is_favourite')
    inlines = [PromptBoxDialogueInline]

admin.site.register(PromptBoxDialogue)
