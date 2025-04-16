
from django.contrib import admin
from django.urls import path,include
from rest_framework.routers import DefaultRouter

from user_api.views import UserProfileViewSet , UserLoginApiView
from promptbox_api.views import PromptBoxItemViewSet


router = DefaultRouter()
router.register('user', UserProfileViewSet, basename='user')
router.register('promptbox', PromptBoxItemViewSet , basename='promptbox')



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', UserLoginApiView.as_view()),
    path('api/' , include(router.urls)),
    path('api/', include('chatbot_api.urls')),
]