from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,reverse
from rest_framework.permissions import AllowAny

from django.contrib.auth import get_user_model

from account.serializers import (
    SignupSerializer, OTPVerifySerializer
)
User = get_user_model()

# =========================
# Signup API
# =========================
class SignupAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()

            return Response({
                "success": True,
                "message": "User created. OTP sent.",
                "user_id": user.id
            }, status=status.HTTP_201_CREATED)

        return Response({
            "success": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)



# OTP Verify APIView
class OTPVerifyAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data["user"]

            return Response({
                "success": True,
                "message": "Account verified successfully",
                "user_id": user.id
            }, status=status.HTTP_200_OK)

        return Response({
            "success": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

# Login APIView