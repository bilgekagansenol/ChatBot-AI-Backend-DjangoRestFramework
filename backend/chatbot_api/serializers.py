from rest_framework import serializers

from chatbot_api.models import ChatSession, ChatMessage



class ChatMessageSerializer(serializers.ModelSerializer):
    """serializer  for session model"""
    class Meta:
        model = ChatMessage
        fields = '__all__'
        read_only_fields = ['timestamp','token_usage','response_time']

    def get_chart_image_url(self, obj):
            request = self.context.get("request")
            if obj.chart_image and hasattr(obj.chart_image, "url"):
                return request.build_absolute_uri(obj.chart_image.url) if request else obj.chart_image.url
            return None
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