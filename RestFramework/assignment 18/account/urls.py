# account/urls.py
from django.urls import path
from account.views import (
    APIEndpoints, SignupAPIView, OTPVerifyAPIView,
)

urlpatterns = [
    path('', APIEndpoints.as_view(), name='api-endpoints'),
    path('signup/', SignupAPIView.as_view(), name='signup'),
    path('otp-verify/', OTPVerifyAPIView.as_view(), name='otp-verify'),
]   