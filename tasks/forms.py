from django import forms
from .models import Task, Assignment

DAYS_OF_WEEK = [
    ('monday', 'Monday'),
    ('tuesday', 'Tuesday'),
    ('wednesday', 'Wednesday'),
    ('thursday', 'Thursday'),
    ('friday', 'Friday')
]

class TaskForm(forms.ModelForm):
    days_of_week = forms.MultipleChoiceField(
        choices=DAYS_OF_WEEK,
        widget=forms.CheckboxSelectMultiple,
        required=True,  # Ensure it's required
        label="Days of the Week"  # Comma was missing here
    )
    
    class Meta:
        model = Task
        fields = ['title', 'description', 'why_important', 'expected_result', 'frequency', 'days_of_week', 'task_image', 'next_run']

    def save(self, commit=True):
        # Get the form data
        instance = super(TaskForm, self).save(commit=False)
        selected_days = self.cleaned_data.get('days_of_week', [])
        
        # Convert selected days to JSON format
        days_dict = {day: (day in selected_days) for day, _ in DAYS_OF_WEEK}
        instance.days_of_week = days_dict
        
        if commit:
            instance.save()
        return instance

class AssignmentCompletionForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['observations', 'completion_image']