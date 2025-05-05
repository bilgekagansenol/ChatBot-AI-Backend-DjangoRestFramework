from rest_framework import serializers
from user_api import models

from django.contrib.auth import get_user_model

User = get_user_model()

class ChangePasswordSerailizer(serializers.Serializer):
    """password changing serializer with safety"""
    old_password = serializers.CharField(required = True)
    new_password = serializers.CharField(required=True)


    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is not correct")
        return value
    
    def validate_new_password(self ,value):
        if len(value)< 6:
            raise serializers.ValidationError("new password must be at least 6 characters")
        return value
    




class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes a user profile object"""
    
    class Meta:
        model = models.UserProfile
        fields = ('id' ,'email' ,  'name', 'password','profile_picture')
        extra_kwargs={
            'password':{
                'write_only': True,
                'style':{'input_type': 'password'}
            }
        }

    def create (self , validated_data):
        """create and return a new user"""
        user = models.UserProfile.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password = validated_data['password']
        )

        return user
    

    


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        """check whose email is this"""
        if not User.objects.filter(email=value).exists():
           raise serializers.ValidationError('No user with this email')
        return value
    

    
