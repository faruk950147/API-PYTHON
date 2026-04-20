from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from account.models import OTP
from account.tasks import send_otp_email, resend_otp_email

User = get_user_model()


# =========================
# SIGNUP
# =========================
class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "phone", "password", "password2"]

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError("Password mismatch")
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")

        user = User.objects.create_user(**validated_data)

        result, otp_code = OTP.create_otp(user, "signup")

        if not result["success"]:
            raise serializers.ValidationError(result.get("message"))

        otp_obj = OTP.objects.filter(user=user, otp_type="signup").order_by("-created_at").first()

        if otp_obj:
            send_otp_email.delay(otp_obj.id, otp_code)

        return user


# =========================
# OTP VERIFY (SIGNUP)
# =========================
class OTPVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()

    def validate(self, attrs):
        try:
            user = User.objects.get(email=attrs["email"])
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found")

        if user.is_verified:
            raise serializers.ValidationError("Already verified")

        result = OTP.verify_otp(user, attrs["otp"], "signup")

        if not result["success"]:
            raise serializers.ValidationError(result["message"])

        self.user = user
        return attrs


# =========================
# LOGIN
# =========================
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = authenticate(username=attrs["username"], password=attrs["password"])

        if not user:
            raise serializers.ValidationError("Invalid credentials")

        if not user.is_active:
            raise serializers.ValidationError("Inactive user")

        if not user.is_verified:
            raise serializers.ValidationError("Not verified")

        self.user = user
        return attrs

    def get_tokens(self):
        refresh = RefreshToken.for_user(self.user)

        return {
            "user_id": self.user.id,
            "username": self.user.username,
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }


# =========================
# CHANGE PASSWORD
# =========================
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()
    confirm_password = serializers.CharField()

    def validate(self, attrs):
        user = self.context["request"].user

        if not user.check_password(attrs["old_password"]):
            raise serializers.ValidationError("Wrong old password")

        if attrs["new_password"] != attrs["confirm_password"]:
            raise serializers.ValidationError("Password mismatch")

        self.user = user
        return attrs

    def save(self):
        self.user.set_password(self.validated_data["new_password"])
        self.user.save(update_fields=["password"])
        return self.user


# =========================
# RESET PASSWORD REQUEST
# =========================
class ResetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        try:
            user = User.objects.get(email=attrs["email"])
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found")

        result, otp_code = OTP.create_otp(user, "reset")

        if not result["success"]:
            raise serializers.ValidationError(result.get("message"))

        otp_obj = OTP.objects.filter(user=user, otp_type="reset").order_by("-created_at").first()

        if otp_obj:
            send_otp_email.delay(otp_obj.id, otp_code)

        self.user = user
        return attrs


# =========================
# RESET OTP VERIFY
# =========================
class ResetPasswordOTPVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()

    def validate(self, attrs):
        try:
            user = User.objects.get(email=attrs["email"])
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found")

        result = OTP.verify_otp(user, attrs["otp"], "reset")

        if not result["success"]:
            raise serializers.ValidationError(result["message"])

        self.user = user
        return attrs


# =========================
# SET NEW PASSWORD
# =========================
class SetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    confirm_password = serializers.CharField()

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match")

        try:
            user = User.objects.get(email=attrs["email"])
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found")

        self.user = user
        return attrs

    def save(self):
        self.user.set_password(self.validated_data["password"])
        self.user.save(update_fields=["password"])
        return self.user


# =========================
# RESEND OTP
# =========================
class ResendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        try:
            user = User.objects.get(email=attrs["email"])
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found")

        result, otp_code = OTP.create_otp(user, "signup")

        if not result["success"]:
            raise serializers.ValidationError(result.get("message"))

        otp_obj = OTP.objects.filter(user=user, is_used=False).order_by("-created_at").first()

        if otp_obj:
            resend_otp_email.delay(otp_obj.id)

        self.user = user
        return attrs