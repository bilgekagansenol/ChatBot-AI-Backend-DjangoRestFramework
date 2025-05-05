from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from user_api import serializers
from user_api import models
from user_api.serializers import ChangePasswordSerailizer , PasswordResetRequestSerializer , UserProfileSerializer
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.parsers import MultiPartParser, FormParser

from user_api import permissions

User = get_user_model()
token_generator = PasswordResetTokenGenerator()

class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profiles"""
    serializer_class = serializers.UserProfileSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes=(permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name','email',)

    def get_queryset(self):
        """only own profile is visible"""
        return models.UserProfile.objects.filter(id=self.request.user.id)

class UserLoginApiView(ObtainAuthToken):
    """handle creating user authentication tokens"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self , request):
        serializer = ChangePasswordSerailizer(
            data  = request.data,
            context={'request':request}# sending user to serializer
        )

        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"message":"Password changed successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)



class PasswordResetRequestView(APIView):
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.get(email=email)

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = token_generator.make_token(user)

            reset_url = f"http://localhost:8000/api/reset-password-confirm/?uid={uid}&token={token}"
            send_mail(
                subject="request of resetting Password",
                message=f"click that link to reset your password:\n{reset_url}",
                from_email="blgkgnsnl@gmail.com",  
                recipient_list=[user.email],
                fail_silently=False,
            )
            print("\n Ressetting password link (on console):")
            print(reset_url)


            return Response({"message":"if this email exists password reset link has been sent."})
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
    


from django.utils.http import urlsafe_base64_decode

class PasswordResetConfirmView(APIView):
    def post(self, request):
        uidb64 = request.data.get("uid")
        token = request.data.get("token")
        new_password = request.data.get("new_password")

        if not (uidb64 and token and new_password):
            return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"error": "Invalid UID"}, status=status.HTTP_400_BAD_REQUEST)

        if not token_generator.check_token(user, token):
            return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)

        if len(new_password) < 6:
            return Response({"error": "Password must be at least 6 characters long."}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)


class UploadProfilePictureView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser,FormParser]

    def patch(self , request):
        user = request.user
        profile_picture = request.FILES.get('profile_picture')
        
        if not profile_picture:
            return Response({"error":"No file provided."},status=status.HTTP_400_BAD_REQUEST)

        user.profile_picture = profile_picture
        user.save()

        return Response({"message":"Profile picture updated.","profile_picture":user.profile_picture.url},status=status.HTTP_200_OK)
    