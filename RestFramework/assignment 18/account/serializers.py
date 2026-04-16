from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from account.models import OTP

User = get_user_model()


# ================= SIGNUP =================
from rest_framework import serializers
from django.contrib.auth import get_user_model
from account.models import OTP

User = get_user_model()

# ================= SIGNUP =================
class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "phone", "password", "password2"]

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError("Passwords do not match")
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")

        user = User.objects.create_user(**validated_data)

        result = OTP.create_otp(user)

        if not result["success"]:
            raise serializers.ValidationError(result["message"])

        return {
            "user": user,
            "otp_id": result["otp_id"]
        }


# ================= OTP VERIFY =================
class OTPVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

    def validate(self, attrs):
        email = attrs.get("email")
        otp_code = attrs.get("otp")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found")

        result = OTP.verify_otp(user, otp_code)

        if not result["success"]:
            raise serializers.ValidationError(result["message"])

        attrs["user"] = user
        return attrs


# ================= LOGIN =================
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = authenticate(
            username=attrs["username"],
            password=attrs["password"]
        )

        if not user:
            raise serializers.ValidationError("Invalid credentials")

        if not user.is_verified:
            raise serializers.ValidationError("Account not verified")

        # JWT TOKEN
        refresh = RefreshToken.for_user(user)

        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }
        

class ResendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        email = attrs.get("email")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found")

        result = OTP.create_otp(user)

        if not result["success"]:
            raise serializers.ValidationError(result["message"])

        attrs["user"] = user
        attrs["otp_id"] = result["otp_id"]

        return attrs