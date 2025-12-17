from django.contrib import admin
from courses.models import Addmission

# Register your models here.
@admin.register(Addmission)
class AddmissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'roll', 'cgpa')
    list_per_page = 10
    search_fields = ('name', 'roll')
    list_filter = ('name', 'roll')
    list_editable = ('name', 'roll', 'cgpa')