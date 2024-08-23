from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    why_important = models.TextField()
    expected_result = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_tasks")
    frequency = models.CharField(max_length=50, choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly')])
    next_run = models.DateTimeField()
    task_image = models.ImageField(upload_to='task_images/', null=True, blank=True)
    days_of_week = models.JSONField(default=dict)
    def regenerate(self):
        # Regenerate based on the frequency and update the next_run field
        if self.frequency == 'daily':
            self.next_run += timedelta(days=1)
        elif self.frequency == 'weekly':
            self.next_run += timedelta(weeks=1)
        elif self.frequency == 'monthly':
            self.next_run += timedelta(weeks=4)
        self.save()

class Assignment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="assigned_tasks")
    completed = models.BooleanField(default=False)
    observations = models.TextField(null=False, blank=False)
    completion_image = models.ImageField(upload_to='completion_images/', null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)