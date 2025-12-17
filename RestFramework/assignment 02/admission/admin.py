from django.contrib import admin
from admission.models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'roll', 'cgpa', 'created_at', 'updated_at')
    list_per_page = 10
