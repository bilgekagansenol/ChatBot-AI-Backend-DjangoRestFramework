import requests

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status , permissions

from chatbot_api.models import ChatMessage ,ChatSession
from chatbot_api.serializers import ChatMessageSerializer



class ChatMessageAPIView(APIView):
    """user send message to Ollama and gets return"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request , session_id):
        user = request.user
        message_text = request.data.get("message")

        if not message_text:
            return Response({'error':'Message is required.'},status=status.HTTP_400_BAD_REQUEST)


        #Session control

        try:
            session = ChatSession.objects.get(id=session_id , user=request.user)
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
        ollama_url = "https://997b-176-54-197-20.ngrok-free.app/api/chat"# Ollama URL
        payload = {
            "model": "llama3.2:1b",  # model name
            "messages": formatted_history,
            "stream": False
        }

        try:
            response = requests.post(ollama_url, json=payload)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"OLLAMA HATASI: {e}")  # ekle
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


class  CreateSessionAPIView(APIView):

    def post(self, request):
        session = ChatSession.objects.create(
            user = request.user
        )
        return Response({"session_id": session.id})
    


class ChatSessionMessagesAPIView(APIView):

    def get(self,request ,session_id):
        try:
            session = ChatSession.objects.get(id=session_id , user = request.user)
        except ChatSession.DoesNotExist:
            return Response({'error':'session is not found'},status=status.HTTP_404_NOT_FOUND)
        
        messages = session.messages.order_by('timestamp')
        serialized = ChatMessageSerializer(messages, many= True)

        return Response(serialized.data , status=status.HTTP_200_OK)
    

class ChatSessionListAPIView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        sessions = ChatSession.objects.filter(user= request.user).order_by("-id")
        data = [{"id": s.id, "created": s.created_on} for s in sessions]
        return Response(data, status=status.HTTP_200_OK)