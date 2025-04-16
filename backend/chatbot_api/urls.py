from django.urls import path
from chatbot_api.views.chat_message_view import ChatMessageAPIView


urlpatterns = [
    path('chat/send/<int:session_id>/',ChatMessageAPIView.as_view(),name='chat-message'),
]
