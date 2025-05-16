# stocksimulator/views.py
# views.py
from django.http import JsonResponse
import json


def swagger_json_view(request):
    # Path to your OpenAPI JSON file
    with open('path_to_your_openapi.json', 'r') as f:
        swagger_data = json.load(f)
    return JsonResponse(swagger_data)