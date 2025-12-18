from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import Admission

@admin.register(Admission)
class AdmissionAdmin(admin.ModelAdmin):
    # List display in admin
    list_display = ('id', 'name', 'dob', 'gpa', 'qualification', 'gender', 'department', 'status', 'created_at', 'updated_at')
    
    # Fields to filter by
    list_filter = ('qualification', 'gender', 'department', 'status')
    
    # Searchable fields
    search_fields = ('name', 'department', 'qualification')
    
    # Readonly fields for created/updated timestamps
    readonly_fields = ('created_at', 'updated_at')
    
    # Field grouping in forms
    fieldsets = (
        ('Personal Information', {
            'fields': ('id', 'name', 'dob', 'gender')
        }),
        ('Academic Information', {
            'fields': ('gpa', 'qualification', 'department')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    # Optional: Customize save to show validation errors nicely
    def save_model(self, request, obj, form, change):
        try:
            obj.full_clean()
            super().save_model(request, obj, form, change)
        except ValidationError as e:
            form.add_error(None, e)
