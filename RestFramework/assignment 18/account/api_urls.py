from django.urls import path
from account.api_views import*

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("otp/verify/signup/", OTPVerifyView.as_view(), name="verify-account-otp"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),

    path("password/change/", ChangePasswordView.as_view(), name="change-password"),

    path("password/reset/request/", ResetPasswordRequestView.as_view(), name="reset-password"),
    path("otp/verify/reset/", ResetPasswordOTPVerifyView.as_view(), name="verify-reset-otp"),
    path("password/reset/set/", SetPasswordView.as_view(), name="set-password"),

    path("otp/resend/", ResendOTPView.as_view(), name="resend-otp"),
]