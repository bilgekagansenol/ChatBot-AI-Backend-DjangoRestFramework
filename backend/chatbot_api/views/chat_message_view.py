import requests

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status , permissions

from chatbot_api.models import ChatMessage ,ChatSession
from chatbot_api.serializers import ChatMessageSerializer



class ChatMessageAPIView(APIView):
    """user sendsd message to Ollama and gets return"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request , session_id):
        user = request.user
        message_text = request.data.get("message")

        if not message_text:
            return Response({'error':'Message is required.'},status=status.HTTP_400_BAD_REQUEST)


        #Session control

        try:
            session_id = ChatSession.objects.get(id=session_id , user=session_id)
        except ChatSession.DoesNotExist:
            return Response({'error':'session is not found'}, status=status.HTTP_400_BAD_REQUEST)
        

        #  sace user message

        user_msg = ChatMessage.objects.create(
            session = session,
            is_user = True,
            message = message_text
        )

        # collect old messages 

        past_messages = session.messages.order_by("timestamp")
        formatted_history = [
            {
                "role":"user" if msg.is_user else "assistant",
                "content":msg.message
            } for msg in past_messages
        ]

        #  request to ollama
        ollama_url = "http://localhost:11434/api/chat"  # Ollama URL
        payload = {
            "model": "llama3.2",  # model name
            "messages": formatted_history,
            "stream": False
        }

        try:
            response = requests.post(ollama_url, json=payload)
            response.raise_for_status()
        except requests.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_502_BAD_GATEWAY)

        # 5. take back and save message
        bot_reply = response.json().get("message", {}).get("content", "not answering")
        bot_msg = ChatMessage.objects.create(
            session=session,
            is_user=False,
            message=bot_reply
        )

        # 6. JSON response
        return Response({
            "user_message": ChatMessageSerializer(user_msg).data,
            "bot_reply": ChatMessageSerializer(bot_msg).data
        }, status=status.HTTP_201_CREATED)



