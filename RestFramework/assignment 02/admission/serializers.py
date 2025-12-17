from rest_framework import serializers
from admission.models import Addmission

class AddmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Addmission
        fields = '__all__'