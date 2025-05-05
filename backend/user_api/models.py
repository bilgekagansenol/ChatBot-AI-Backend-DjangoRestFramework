from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.core.validators import FileExtensionValidator

from django.conf import settings


class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""


    def create_user (self, email , name , password = None):
        """create a new user profile"""
        if not email:
            raise ValueError('users must have an email adress')
        
        email = self.normalize_email(email)
        user = self.model(email=email , name = name)
        user.set_password(password)
        user.save(using = self._db)

        return user
    
    def create_superuser(self , email , name , password):
        """create a superuser profile"""
        user = self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user




class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for user in the system"""
    email = models.EmailField(max_length=255 , unique= True)
    name = models.CharField(max_length=255)
    is_active= models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    profile_picture = models.ImageField(
        upload_to="profile_pictures/",
        null=True,
        blank=True,
        validators=[FileExtensionValidator(["jpg", "jpeg", "png"])],
    )
    objects = UserProfileManager()

    USERNAME_FIELD =  'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """retrieve full name of user """
        return self.name
    
    def get_short_name(self):
        """retrieve short name of user"""
        return self.name # for now  just name 
    
    def __str__(self):
        """return string representation of our user"""
        return self.email
    
