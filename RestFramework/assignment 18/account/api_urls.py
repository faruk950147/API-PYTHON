from django.urls import path
from account.api_views import*

urlpatterns = [
    path("signup/", SignupView.as_view()),
    path("otp/verify/signup/", OTPVerifyView.as_view()),
    path("login/", LoginView.as_view()),
    path("logout/", LogoutView.as_view()),

    path("password/change/", ChangePasswordView.as_view()),

    path("password/reset/request/", ResetPasswordRequestView.as_view()),
    path("otp/verify/reset/", ResetPasswordOTPVerifyView.as_view()),
    path("password/reset/set/", SetPasswordView.as_view()),

    path("otp/resend/", ResendOTPView.as_view()),
]