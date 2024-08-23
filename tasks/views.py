from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Task, Assignment
from .serializers import TaskSerializer, AssignmentSerializer
from .forms import TaskForm, DAYS_OF_WEEK, AssignmentCompletionForm
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated
from datetime import datetime

# API ViewSets
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access the API

class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access the API


# Views for HTML-based interface
def home(request):
    return render(request, 'tasks/dashboard.html')


@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES)
        
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            
            # Ensure days_of_week is processed correctly
            selected_days = form.cleaned_data.get('days_of_week', [])
            print("Selected days:", selected_days)  # Debugging line
            
            if not selected_days:
                # This will trigger if no days are selected
                form.add_error('days_of_week', 'Please select at least one day.')
            else:
                # Convert the selected days into a JSON-compatible dictionary format
                days_dict = {day: (day in selected_days) for day, _ in DAYS_OF_WEEK}
                task.days_of_week = days_dict
                print("Days of week set:", days_dict)  # Debugging line
                
                # Set the initial next_run time
                task.next_run = datetime.now()
                task.save()
                return redirect('dashboard')
        else:
            # Debugging form errors
            print("Form errors:", form.errors)
    else:
        form = TaskForm()

    return render(request, 'tasks/create_task.html', {'form': form})

@login_required
def dashboard(request):
    # Include tasks that either have no assignments or have incomplete assignments
    incomplete_tasks = Task.objects.filter(assignment__completed=False).distinct() | Task.objects.filter(assignment__isnull=True).distinct()
    
    # Include tasks that have been completed
    completed_tasks = Task.objects.filter(assignment__completed=True).distinct()

    return render(request, 'tasks/dashboard.html', {
        'incomplete_tasks': incomplete_tasks,
        'completed_tasks': completed_tasks,
    })


@login_required
def assign_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    
    if request.method == 'POST':
        user_id = request.POST.get('user')
        user = get_object_or_404(User, id=user_id)
        
        # Check if there is already an incomplete assignment for this task and user
        existing_assignment = Assignment.objects.filter(task=task, assigned_to=user, completed=False).first()
        
        if existing_assignment:
            # Optionally, do nothing or reassign
            pass
        else:
            # If no incomplete assignment exists, create a new one
            Assignment.objects.create(task=task, assigned_to=user)
        
        return redirect('dashboard')
    
    users = User.objects.all()
    return render(request, 'tasks/assign_task.html', {'task': task, 'users': users})


@login_required
def complete_task(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    
    if request.method == 'POST':
        form = AssignmentCompletionForm(request.POST, request.FILES, instance=assignment)
        if form.is_valid():
            assignment.completed = True
            assignment.completed_at = datetime.now()
            form.save()
            
            # Do NOT regenerate immediately, just update the task's next run date
            task = assignment.task
            task.regenerate()  # This updates the task's next_run based on the frequency
            
            return redirect('dashboard')
    else:
        form = AssignmentCompletionForm(instance=assignment)
    
    return render(request, 'tasks/complete_task.html', {'form': form})

@login_required
def task_details(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    return render(request, 'tasks/task_details.html', {'assignment': assignment})