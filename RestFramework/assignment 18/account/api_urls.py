# account/urls.py
from django.urls import path
from account.api_views import (
    SignupAPIView, OTPVerifyAPIView
)

urlpatterns = [
    path('signup/', SignupAPIView.as_view()),
    path('verify-otp/', OTPVerifyAPIView.as_view()),
]   