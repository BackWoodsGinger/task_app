from rest_framework import serializers
from .models import Task, Assignment

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description', 'why_important', 'expected_result', 'created_by', 'frequency', 'days_of_week', 'next_run', 'task_image']

class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ['task', 'assigned_to', 'completed', 'observations', 'completion_image']
