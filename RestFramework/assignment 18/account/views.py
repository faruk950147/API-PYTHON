# account/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import login, logout
from django.core.exceptions import ValidationError

from account.serializers import (
    SignupSerializer, OTPVerifySerializer,
)
from account.utils import send_otp_email

class APIEndpoints(APIView):
    def get(self, request):
        return Response({
            "endpoints": {
                "signup": "api/account/signup/",
                "otp_verify": "api/account/otp-verify/",
                "login": "api/account/login/",
                "logout": "api/account/logout/",
                "password_change": "api/account/password-change/",
                "password_reset_request": "api/account/password-reset-request/",
                "password_reset_verify": "api/account/password-reset-verify/",
            }
        })


# Signup APIView
class SignupAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # OTP sending is already handled in serializer
        otp_error = getattr(user, "_otp_error", None)
        if otp_error:
            return Response({"detail": f"User created, but OTP not sent: {otp_error}"}, status=status.HTTP_201_CREATED)
        return Response({"detail": "User created, OTP sent"}, status=status.HTTP_201_CREATED)

# OTP Verify APIView
class OTPVerifyAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"detail": "OTP verified successfully"}, status=status.HTTP_200_OK)

# Login APIView
