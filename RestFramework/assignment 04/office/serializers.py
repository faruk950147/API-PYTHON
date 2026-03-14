from rest_framework import serializers
from office.models import Company, Department, Employee
"""
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
        fields = "__all__" """
        
class CompanyHyperlinkedSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='company-detail')  # url field add
    
    class Meta:
        model = Company
        fields = ['url', 'id', 'name', 'address', 'phone', 'email', 'website', 'industry','created_at', 'updated_at']


class DepartmentHyperlinkedSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='department-detail')
    company = serializers.HyperlinkedRelatedField(
        view_name='company-detail',
        read_only=True
    )
    
    class Meta:
        model = Department
        fields = ['url', 'id', 'company', 'name', 'description', 'created_at', 'updated_at']


class EmployeeHyperlinkedSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='employee-detail')
    company = serializers.HyperlinkedRelatedField(
        view_name='company-detail',
        read_only=True
    )
    department = serializers.HyperlinkedRelatedField(
        view_name='department-detail',
        read_only=True
    )
    
    class Meta:
        model = Employee
        fields = [
            'url', 'id', 'company', 'department', 'first_name', 'last_name', 'email', 'phone',
            'position', 'hire_date', 'salary', 'is_active', 'created_at', 'updated_at'
        ]