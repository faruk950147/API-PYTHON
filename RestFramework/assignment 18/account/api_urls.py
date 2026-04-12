# account/urls.py
from django.urls import path
from account.api_views import (
    APIEndpoints, SignupAPIView, OTPVerifyAPIView
)

urlpatterns = [
    path('', APIEndpoints.as_view()),
    path('signup/', SignupAPIView.as_view()),
    path('verify-otp/', OTPVerifyAPIView.as_view()),
]   