from django.contrib import admin
from office.models import Employee

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'department', 'dob', 'created_at', 'updated_at')
    search_fields = ('name', 'email', 'department')
    list_filter = ('department', 'created_at')
    ordering = ('-created_at',)