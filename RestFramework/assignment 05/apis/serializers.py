from rest_framework import serializers
from apis.models import Student
from datetime import date


class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = '__all__'
