from django.contrib import admin
from apis.models import Admission
# Register your models here.
@admin.register(Admission)
class AdmissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'dob', 'gpa', 'qualification', 'gender', 'department', 'status', 'created_at', 'updated_at')
    list_filter = ('qualification', 'gender', 'department', 'status')
    search_fields = ('name', 'department', 'qualification')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('name', 'dob', 'gpa', 'qualification', 'gender', 'department', 'status')
        }),
    )