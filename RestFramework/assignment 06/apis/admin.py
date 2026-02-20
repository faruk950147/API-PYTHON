from django.contrib import admin
from apis.models import Student
# Register your models here.
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'dob', 'status', 'created_at', 'updated_at')
    list_filter = ('id', 'status')
    search_fields = ('id', 'name',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('name', 'dob', 'status')
        }),
    )