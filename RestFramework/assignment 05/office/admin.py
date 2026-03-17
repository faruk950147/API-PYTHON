from django.contrib import admin
from office.models import Company, Department, Employee

# Company admin (all fields)
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'address', 'phone', 'email',
        'website', 'industry', 'created_at', 'updated_at'
    )
    search_fields = ('name', 'industry', 'email', 'phone', 'website')
    list_filter = ('industry', 'created_at', 'updated_at')
    ordering = ('-created_at',)


# Department admin (all fields)
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'company', 'description',
        'created_at', 'updated_at'
    )
    search_fields = ('name', 'company__name', 'description')
    list_filter = ('company', 'created_at', 'updated_at')
    ordering = ('-created_at',)


# Employee admin (all fields)
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'email', 'phone', 'company', 'department',
        'position', 'salary', 'status', 'hire_date', 'date_of_birth',
        'address', 'created_at', 'updated_at'
    )
    search_fields = (
        'name', 'email', 'phone', 'company__name', 'department__name',
        'position', 'address'
    )
    list_filter = ('company', 'department', 'status', 'hire_date', 'date_of_birth')
    ordering = ('-created_at',)