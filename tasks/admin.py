from django.contrib import admin
from .models import Task, Assignment

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'frequency', 'next_run', 'days_of_week')  # Customize fields to display
    list_filter = ('created_by', 'frequency', 'next_run')  # Enable filtering
    search_fields = ('title', 'description')  # Enable search functionality
    ordering = ('-next_run',)  # Order by next run date, descending

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('task', 'assigned_to', 'completed', 'completed_at')  # Customize fields to display
    list_filter = ('completed', 'assigned_to', 'completed_at')  # Enable filtering
    search_fields = ('task__title', 'observations')  # Enable search functionality
    ordering = ('-completed_at',)  # Order by completed_at date, descending