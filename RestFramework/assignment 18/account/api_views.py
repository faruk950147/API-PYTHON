from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from account.serializers import *


# =========================
# SIGNUP
# =========================
class SignupView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created. OTP sent."}, status=201)

        return Response(serializer.errors, status=400)


# =========================
# OTP VERIFY
# =========================
class OTPVerifyView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)

        if serializer.is_valid():
            serializer.user.is_verified = True
            serializer.user.save(update_fields=["is_verified"])

            return Response({"message": "Verified successfully"}, status=200)

        return Response(serializer.errors, status=400)


# =========================
# LOGIN
# =========================
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            return Response(serializer.get_tokens(), status=200)

        return Response(serializer.errors, status=400)


# =========================
# LOGIN
# =========================
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logged out"})
        except Exception:
            return Response({"error": "Invalid token"}, status=400)


# =========================
# CHANGE PASSWORD
# =========================
class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={"request": request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password changed"}, status=200)

        return Response(serializer.errors, status=400)


# =========================
# RESET PASSWORD REQUEST
# =========================
class ResetPasswordRequestView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ResetPasswordRequestSerializer(data=request.data)

        if serializer.is_valid():
            return Response({"message": "OTP sent"}, status=200)

        return Response(serializer.errors, status=400)


# =========================
# RESET OTP VERIFY
# =========================
class ResetPasswordOTPVerifyView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ResetPasswordOTPVerifySerializer(data=request.data)

        if serializer.is_valid():
            return Response({"message": "OTP verified"}, status=200)

        return Response(serializer.errors, status=400)


# =========================
# SET NEW PASSWORD
# =========================
class SetPasswordView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = SetPasswordSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password reset successful"}, status=200)

        return Response(serializer.errors, status=400)


# =========================
# RESEND OTP
# =========================
class ResendOTPView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ResendOTPSerializer(data=request.data)

        if serializer.is_valid():
            return Response({"message": "OTP resent"}, status=200)

        return Response(serializer.errors, status=400)