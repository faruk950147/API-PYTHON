from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from account.serializers import(
    SignupSerializer,
    OTPVerifySerializer,
    LoginSerializer,
    ResendOTPSerializer
)

# ================= SIGNUP =================
class SignupView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        serializer = SignupSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            return Response({
                "message": "Signup successful. Please verify your email.",
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ================= VERIFY OTP =================
class VerifyOTPView(APIView):
    permission_classes = [permissions.AllowAny]


    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)

        if serializer.is_valid():
            return Response({"message": "You are verified"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ================= LOGIN =================
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ================= LOGOUT =================


# ================= Resend OTP =================
class ResendOTPView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ResendOTPSerializer(data=request.data)

        if serializer.is_valid():
            return Response({
                "success": True,
                "message": "OTP resent successfully",
                "otp_id": serializer.validated_data["otp_id"]
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ================= PROTECTED =================
class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user

        return Response({
            "username": user.username,
            "email": user.email,
            "verified": user.is_verified
        })