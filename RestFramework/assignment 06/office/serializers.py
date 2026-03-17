from rest_framework import serializers
from office.models import Company, Department, Employee
        
# Company Serializer
class CompanyHyperlinkedSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='company-detail')  # url field add
    
    class Meta:
        model = Company
        fields = [
            'url', 'id', 'name', 'address', 'phone', 'email', 
            'website', 'industry', 'created_at', 'updated_at'
        ]

# Department Serializer
class DepartmentHyperlinkedSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='department-detail')
    company = serializers.HyperlinkedRelatedField(
        view_name='company-detail',
        read_only=True
    )
    
    class Meta:
        model = Department
        fields = [
            'url', 'id', 'company', 'name', 'description', 
            'created_at', 'updated_at'
        ]

# Employee Serializer
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
            'url', 'id', 'company', 'department', 'name', 'email', 
            'phone', 'position', 'hire_date', 'salary', 'status', 
            'created_at', 'updated_at'
        ]