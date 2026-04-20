from django.urls import path
from account.api_views import (
    SignupView,
    OTPVerifyView,
    LoginView,
    LogoutView,
    ChangePasswordView,
    ResetPasswordRequestView,
    ResetPasswordOTPVerifyView,
    SetPasswordView,
    ResendOTPView
)

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("verify-account-otp/", OTPVerifyView.as_view(), name="verify-account-otp"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),

    path("change-password/", ChangePasswordView.as_view(), name="change-password"),

    path("reset-password/", ResetPasswordRequestView.as_view(), name="reset-password"),
    path("verify-reset-otp/", ResetPasswordOTPVerifyView.as_view(), name="verify-reset-otp"),
    path("set-password/", SetPasswordView.as_view(), name="set-password"),

    path("resend-otp/", ResendOTPView.as_view(), name="resend-otp"),
]