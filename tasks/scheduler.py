from apscheduler.schedulers.background import BackgroundScheduler
from .models import Task
from datetime import datetime

def regenerate_tasks():
    # Get the current day in lowercase
    today = datetime.now().strftime('%A').lower()
    
    # Find tasks that are due for regeneration (i.e., next_run is in the past or now)
    tasks = Task.objects.filter(next_run__lte=datetime.now())
    
    for task in tasks:
        # Check if the task should regenerate today based on the days_of_week field
        if task.days_of_week.get(today):
            # Regenerate the task by updating the next_run time according to its frequency
            task.regenerate()

def start_scheduler():
    scheduler = BackgroundScheduler()
    # Schedule the regenerate_tasks function to run every 60 minutes
    scheduler.add_job(regenerate_tasks, 'interval', minutes=60)
    scheduler.start()