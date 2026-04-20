from django.urls import path
from account.api_views import *

urlpatterns = [
    path("signup/", SignupView.as_view()),
    path("verify-account-otp/", OTPVerifyView.as_view()),
    path("login/", LoginView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("change-password/", ChangePasswordView.as_view()),
    path("reset-password/", ResetPasswordRequestView.as_view()),
    path("verify-reset-otp/", ResetPasswordOTPVerifyView.as_view()),
    path("set-password/", SetPasswordView.as_view()),
    path("resend-otp/", ResendOTPView.as_view()),
]