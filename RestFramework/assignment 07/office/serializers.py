from rest_framework import serializers
from office.models import Company, Department, Employee

# Company Serializer
class CompanyHyperlinkedSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the Company model using HyperlinkedModelSerializer.
    
    Fields:
        url (HyperlinkedIdentityField): Hyperlinked URL for company detail view
        id (IntegerField): Primary key
        name (CharField): Company name
        address (CharField): Company address
        phone (CharField): Company phone number
        email (EmailField): Company email
        website (URLField): Company website
        industry (CharField): Industry type
        created_at (DateTimeField): Timestamp when company was created
        updated_at (DateTimeField): Timestamp when company was last updated
    """
    url = serializers.HyperlinkedIdentityField(view_name='company-detail')
    
    class Meta:
        model = Company
        fields = [
            'url', 'id', 'name', 'address', 'phone', 'email',
            'website', 'industry', 'created_at', 'updated_at'
        ]


# Department Serializer
class DepartmentHyperlinkedSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the Department model using HyperlinkedModelSerializer.
    
    Fields:
        url (HyperlinkedIdentityField): Hyperlinked URL for department detail view
        company (HyperlinkedRelatedField): Related company URL (read-only)
        id (IntegerField): Primary key
        name (CharField): Department name
        description (CharField): Department description
        created_at (DateTimeField): Timestamp when department was created
        updated_at (DateTimeField): Timestamp when department was last updated
    """
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
    """
    Serializer for the Employee model using HyperlinkedModelSerializer.
    
    Fields:
        url (HyperlinkedIdentityField): Hyperlinked URL for employee detail view
        company (HyperlinkedRelatedField): Related company URL (read-only)
        department (HyperlinkedRelatedField): Related department URL (read-only)
        id (IntegerField): Primary key
        name (CharField): Employee name
        email (EmailField): Employee email
        phone (CharField): Employee phone number
        position (CharField): Job position
        hire_date (DateField): Date of hire
        salary (DecimalField): Employee salary
        status (CharField): Active/inactive status
        created_at (DateTimeField): Timestamp when employee was created
        updated_at (DateTimeField): Timestamp when employee was last updated
    """
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