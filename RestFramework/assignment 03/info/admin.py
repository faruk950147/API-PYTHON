from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import Admission

@admin.register(Admission)
class AdmissionAdmin(admin.ModelAdmin):
    # List display in admin (id is fine here)
    list_display = ('id', 'name', 'dob', 'gpa', 'qualification', 'gender', 'department', 'status', 'created_at', 'updated_at')
    
    # Fields to filter by
    list_filter = ('qualification', 'gender', 'department', 'status')
    
    # Searchable fields
    search_fields = ('name', 'department', 'qualification')
    
    # Readonly fields for created/updated timestamps
    readonly_fields = ('created_at', 'updated_at')
