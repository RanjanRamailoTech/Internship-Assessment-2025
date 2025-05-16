
from django.urls import path
from .views import populate_data

urlpatterns = [
    path('populate/', populate_data, name='populate_data')
]
