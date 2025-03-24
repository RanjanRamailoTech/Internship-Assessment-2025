import os
from celery import Celery
from django.conf import settings

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

# Create Celery app
app = Celery('project')

# Load configuration from Django settings with CELERY_ prefix
app.config_from_object('django.conf:settings', namespace='CELERY')

# Debug: Print the broker URL to verify
print("CELERY_BROKER_URL from settings:", getattr(settings, 'CELERY_BROKER_URL', 'Not found'))

# Auto-discover tasks
app.autodiscover_tasks([
    "ramailo.tasks.ramailo_tasks",
    "user.tasks",
])

# Optional debug task
@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')