from rest_framework import serializers
from office.models import Company, Department, Employee

# Company Serializer
class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"

# Department Serializer
class DepartmentSerializer(serializers.ModelSerializer):
    company = serializers.StringRelatedField()
    class Meta:
        model = Department
        fields = "__all__"

# Employee Serializer
class EmployeeSerializer(serializers.ModelSerializer):
    company = serializers.StringRelatedField()
    department = serializers.StringRelatedField()
    
    class Meta:
        model = Employee
        fields = "__all__"