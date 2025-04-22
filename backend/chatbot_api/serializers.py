from rest_framework import serializers

from chatbot_api.models import ChatSession, ChatMessage



class ChatMessageSerializer(serializers.ModelSerializer):
    """serializer  for session model"""
    class Meta:
        model = ChatMessage
        fields = '__all__'
        read_only_fields = ['timestamp','token_usage','response_time']


class SessionSerializer(serializers.ModelSerializer):
    """serializer for chat sessions"""
    messages = ChatMessageSerializer(many=True, read_only = True)


    class Meta:
        model = ChatSession
        fields = '__all__'
        read_only_fields = ['created_on', 'last_uploaded']
    
class UpdateSessionTitleSerializer(serializers.ModelSerializer):
    """serializer for session title update"""
    class Meta:
        model = ChatSession
        fields = ['title']