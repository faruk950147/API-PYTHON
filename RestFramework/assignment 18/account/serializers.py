from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from account.models import OTP
import random

User = get_user_model()

# Signup Serializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from account.models import OTP
from account.utils import send_otp_email
from django.core.exceptions import ValidationError
import random

User = get_user_model()

class SignupSerializer(serializers.ModelSerializer):
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
        try:
            send_otp_email(user)
        except ValidationError as e:
            # OTP generate failed but user created
            # We will handle proper response in API view
            user._otp_error = e.messages[0]
        return user

# OTP Verification Serializer
class OTPVerifySerializer(serializers.ModelSerializer):
    class Meta:
        model = OTP
        fields = [ 'otp_hash']