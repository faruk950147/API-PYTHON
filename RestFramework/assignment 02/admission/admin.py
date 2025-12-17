from django.contrib import admin
from admission.models import Registration


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'roll', 'cgpa', 'created_at', 'updated_at')
    list_per_page = 10
