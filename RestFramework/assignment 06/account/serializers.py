# your_app/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'phone', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True, 'required': True},
            'email': {'required': False},
            'phone': {'required': True},
            'username': {'required': True},
        }

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            phone=validated_data['phone'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
