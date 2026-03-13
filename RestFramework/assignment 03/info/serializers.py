from rest_framework import serializers
from info.models import Admission

class AdmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admission
        fields = '__all__'
        
    def create(self, validated_data):
        return Admission.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.dob = validated_data.get('dob', instance.dob)
        instance.gpa = validated_data.get('gpa', instance.gpa)
        instance.qualification = validated_data.get('qualification', instance.qualification)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.department = validated_data.get('department', instance.department)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance