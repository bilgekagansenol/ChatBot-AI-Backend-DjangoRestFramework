from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings # for user

class ChatSession(models.Model):
    """
    A user  can have multiple chat sessions:

    id 
    user
    created_on
    title(for changing with ai or self)
    last_uploaded
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete= models.CASCADE,
        related_name= 'chat_sessions'
    )
    model_name = models.CharField (max_length=100 , null= True , blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank= True,default='New Chat')
    last_uploaded = models.DateTimeField(auto_now=True)
    is_favourite = models.BooleanField(default=False)

    def __str__(self):
        return f"Session id  = #{self.pk}"
    
    class Meta:
        ordering = ['-last_uploaded']


class ChatMessage(models.Model):
    """
    message class for conversations
    sessions with foreign key
    is_user  control is it bot or user
    message
    timestamp
    token_usage
    response_time
    """

    session = models.ForeignKey(
        ChatSession,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    model_name = models.CharField(max_length=100, null=True, blank=True)
    is_user = models.BooleanField(blank=False)
    message = models.CharField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)
    token_usage = models.IntegerField(null=True , blank=True)#don't show it to user
    response_time = models.FloatField(null=True , blank= True)
    chart_image = models.ImageField(upload_to='chat_charts/', null=True , blank=True)
    

