from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings #for  user model


class PromptBoxItem(models.Model):
    """
    PromptBoxItem model consider: 
    id 
    user
    promptBoxItem_dialogue
    created_on
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='promptbox'
    )
    PromptBoxItem_information = models.CharField(max_length=1000,blank=False ,null = False )
    created_on = models.DateTimeField(auto_now_add=True)
    is_favourite = models.BooleanField(default=False)

    def __str__(self):
        return self.PromptBoxItem_information or f"PromptBoxItem #{self.pk}"


class PromptBoxDialogue(models.Model):
    """it consider prompt and response"""
    promptbox_item = models.ForeignKey(
        PromptBoxItem,
        on_delete=models.CASCADE,
        related_name='dialogue'
    )
    prompt = models.TextField()
    response = models.TextField()
    def clean(self):
        if not self.prompt or not self.response:
            raise ValidationError("prompt and response can't be empty")
        
    def __str__(self):
        return  f"{self.prompt[:300]} → {self.response[:300]}"
    