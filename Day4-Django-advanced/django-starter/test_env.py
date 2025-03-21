import os
from decouple import config

print("os.environ.get('CELERY_BROKER_URL'):", os.environ.get('CELERY_BROKER_URL'))
print("config('CELERY_BROKER_URL'):", config('CELERY_BROKER_URL', default='Not found'))