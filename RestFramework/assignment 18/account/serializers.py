from rest_framework import serializers
from django.contrib.auth import get_user_model
from account.models import OTP
from account.utils import send_otp_email

User = get_user_model()

# Signup Serializer
class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'password', 'password2']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password2'):
            raise serializers.ValidationError("Passwords do not match")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data, is_active=True, is_verified=False)
        
        # OTP Generate & Email
        otp_instance, otp = OTP.create_otp(user, otp_type="register")
        send_otp_email(user, otp)
        
        return user

# OTP Verification Serializer
class OTPVerifySerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    hash_otp = serializers.CharField(max_length=6, write_only=True)  # user input OTP

    def validate(self, attrs):
        email = attrs.get('email')
        hash_otp = attrs.get('hash_otp')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found")

        # Get the latest OTP for this user and type "register"
        try:
            otp_instance = OTP.objects.filter(user=user, otp_type="register").order_by("-created_at")[0]
        except IndexError:
            raise serializers.ValidationError("No OTP found for this user")

        result = otp_instance.verify_otp(hash_otp)  # verify_otp internally hashes it
        if result != "success":
            raise serializers.ValidationError(result)

        return attrs