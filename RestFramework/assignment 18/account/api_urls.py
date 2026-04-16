from django.urls import path
from account.api_views import (
    SignupView, 
    VerifyOTPView, 
    LoginView, 
    ProfileView, 
    ResendOTPView
)

urlpatterns = [
    path("signup/", SignupView.as_view()),
    path("verify-otp/", VerifyOTPView.as_view()),
    path("login/", LoginView.as_view()),
    path("profile/", ProfileView.as_view()),
    path("resend-otp/", ResendOTPView.as_view()),
]