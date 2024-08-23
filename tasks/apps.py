from django.apps import AppConfig

class TasksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tasks'

    def ready(self):
        # Only start the scheduler in the main process to avoid multiple starts
        import os
        if os.environ.get('RUN_MAIN', None) == 'true':
            from .scheduler import start_scheduler
            start_scheduler()