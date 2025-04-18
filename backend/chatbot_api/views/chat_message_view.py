import requests
import time

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
        ollama_url = "https://346d-213-74-176-214.ngrok-free.app/api/chat"# Ollama URL
        payload = {
            "model": "llama3.2:1b",  # model name
            "messages": formatted_history,
            "stream": False
        }

        try:
            start = time.time()
            response = requests.post(ollama_url, json=payload)
            end = time.time()
            response_time = round(end - start , 3)
            response.raise_for_status()
            ## print("OLLLAMA RESPONSE JSON:", response.json())  ## for examine
            ollama_data = response.json()
            token_usage = ollama_data.get("prompt_eval_count", 0) + ollama_data.get("eval_count", 0)
        except requests.RequestException as e:
            print(f"OLLAMA HATASI: {e}")  # ekle
            return Response({"error": str(e)}, status=status.HTTP_502_BAD_GATEWAY)


        # 5. take back and save message
        bot_reply = response.json().get("message", {}).get("content", "not answering")
        bot_msg = ChatMessage.objects.create(
            session=session,
            is_user=False,
            message=bot_reply,
            response_time = response_time,
            model_name = "llama3.2:1b",
            token_usage=token_usage
        )

        # 6. JSON response
        return Response({
            "user_message": ChatMessageSerializer(user_msg).data,
            "bot_reply": ChatMessageSerializer(bot_msg).data
        }, status=status.HTTP_201_CREATED)


class  CreateSessionAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        title = request.data.get('title','')
        session = ChatSession.objects.create(
            user = request.user,
            title = title
        )
        return Response({"session_id": session.id, 'title': session.title})
    


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
        data = [{"id": s.id, "created": s.created_on , 'title': s.title} for s in sessions]
        return Response(data, status=status.HTTP_200_OK)
    

class ChatSessionDeleteAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete (self , request , session_id):
        try:
            session = ChatSession.objects.get(id = session_id , user = request.user)
        except ChatSession.DoesNotExist:
            return Response({"message":"Session not found"}, status=status.HTTP_404_NOT_FOUND)
        
        session.delete()
        return Response({"message":"Session deleted sucessfully"} , status=status.HTTP_200_OK)
    

class UpdateFavouriteAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request  , session_id):
        try:
            session = ChatSession.objects.get(id=session_id , user = request.user)
        except ChatSession.DoesNotExist:
            return Response({"message":"There no session to update its is_favourite field"}, status=status.HTTP_400_BAD_REQUEST)
        
        is_fav = request.data.get('is_favourite')
        if is_fav is None:
            return Response({'error':'missing  is_favourite field'}, status=status.HTTP_400_BAD_REQUEST)
        
        session.is_favourite = is_fav
        session.save()
        return Response({'message':'Session favourite status  updated','is_favourite':session.is_favourite})
