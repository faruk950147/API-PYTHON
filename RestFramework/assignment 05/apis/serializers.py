from rest_framework import serializers
from apis.models import Admission
from datetime import date


class AdmissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Admission
        fields = '__all__'

    # GPA Validation
    def validate_gpa(self, value):
        if value < 3.50:
            raise serializers.ValidationError("GPA must be at least 3.50")
        return value

    # DOB Validation (Minimum age 18)
    def validate(self, attrs):
        dob = attrs.get('dob')
        today = date.today()

        age = today.year - dob.year - (
            (today.month, today.day) < (dob.month, dob.day)
        )

        if age < 18:
            raise serializers.ValidationError(
                {"dob": "Student must be at least 18 years old."}
            )

        return attrs