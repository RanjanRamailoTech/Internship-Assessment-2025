import os
from celery import Celery
from django.conf import settings

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

# Create Celery app
app = Celery('project')

# Load configuration from Django settings with CELERY_ prefix
app.config_from_object('django.conf:settings', namespace='CELERY')


# Load task modules from all registered Django app configs.
app.autodiscover_tasks([
    "stock.tasks.stock_tasks"
])

app.conf.broker_transport_options = {
    'max_retries': 2,
    'interval_start': 0,
    'interval_step': 0.2,
    'interval_max': 0.2,
}

app.conf.beat_schedule = {
    'execute_ramailo_task_in_every_2_min': {
        'task': 'execute_stock_task',
        'schedule': 1 * 60   # Run every 2 min
    },
}