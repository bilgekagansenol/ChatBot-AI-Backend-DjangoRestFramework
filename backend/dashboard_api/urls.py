from django.urls import path
from .views import UserCountAPIView, PromptCountAPIView, WeeklySessionStatsAPIView
from .views import TodaySessionCountAPIView, TopActiveUsersAPIView, TokenUserCountAPIView
urlpatterns = [
    path('user-count/', UserCountAPIView.as_view()),
    path('prompt-count/', PromptCountAPIView.as_view()),
    path('weekly-sessions/', WeeklySessionStatsAPIView.as_view()),
       path('today-sessions/', TodaySessionCountAPIView.as_view()),
    path('top-users/', TopActiveUsersAPIView.as_view()),
    path('token-user-count/', TokenUserCountAPIView.as_view()),
]
