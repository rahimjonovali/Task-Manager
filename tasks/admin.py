from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'due_date', 'user')
    list_filter = ('status', 'due_date', 'user')
    search_fields = ('title', 'description')
    date_hierarchy = 'due_date'

