from django.contrib import admin
from api.models import Task
# Register your models here.
class TaskAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'title','completed'
    ]
    list_editable = ['completed']
admin.site.register(Task, TaskAdmin)