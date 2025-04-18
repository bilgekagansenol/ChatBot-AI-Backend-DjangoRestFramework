from django.urls import path
from chatbot_api.views.chat_message_view import ChatMessageAPIView ,CreateSessionAPIView ,ChatSessionMessagesAPIView , ChatSessionListAPIView  ,ChatSessionDeleteAPIView , UpdateFavouriteAPIView

                                                                                                                                


urlpatterns = [
    path('chat/send/<int:session_id>/',ChatMessageAPIView.as_view(),name='chat-message'),
    path('chat/session/create/', CreateSessionAPIView.as_view() , name='create-session'),
    path('chat/sessions/', ChatSessionListAPIView.as_view(), name='chat-session-list'),
    path('chat/session/<int:session_id>/messages/', ChatSessionMessagesAPIView.as_view(), name='session-messages'),
    path('chat/session/<int:session_id>/delete/', ChatSessionDeleteAPIView.as_view(),name='delete-session'),
    path('chat/session/<int:session_id>/favourite/', UpdateFavouriteAPIView.as_view(),name='update-favourite')
]
