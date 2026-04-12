from rest_framework import serializers
from django.contrib.auth import get_user_model
from account.models import OTP

User = get_user_model()


# =========================
# SIGNUP SERIALIZER
# =========================
class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "phone", "password", "password2"]

    def validate(self, attrs):
        if attrs.get("password") != attrs.get("password2"):
            raise serializers.ValidationError("Passwords do not match")
        return attrs

    def create(self, validated_data):
        password = validated_data.get("password")

        user = User.objects.create_user(
            username=validated_data.get("username"),
            email=validated_data.get("email"),
            phone=validated_data.get("phone"),
            password=password
        )

        OTP.create_otp(user)

        return user



# =========================
# OTP VERIFY SERIALIZER
# =========================
class OTPVerifySerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    otp = serializers.CharField(max_length=6, write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        otp_code = attrs.get("otp")

        # user check
        user = User.objects.filter(email=email).first()
        if not user:
            raise serializers.ValidationError("User not found")

        # latest otp
        otp_obj = OTP.objects.filter(
            user=user,
            is_used=False
        ).order_by("-created_at").first()

        if not otp_obj:
            raise serializers.ValidationError("OTP not found")

        # verify
        result = OTP.verify_otp(otp_obj.id, otp_code)

        if not result["success"]:
            raise serializers.ValidationError(result["message"])

        attrs["user"] = user
        return attrs
