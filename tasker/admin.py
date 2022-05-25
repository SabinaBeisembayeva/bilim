from django.contrib import admin
from tasker.models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'deadline', 'status', 'user')
    search_fields = ('title','user')