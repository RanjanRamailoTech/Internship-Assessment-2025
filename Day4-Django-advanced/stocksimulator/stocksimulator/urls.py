# stocksimulator/urls.py
from django.contrib import admin
from django.urls import path, include
from .swagger_views import swagger_json_view
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from stocksimulator import swagger_views

# Original schema view for /swagger.json/ (for utils.py)
schema_view = get_schema_view(
    openapi.Info(
        title="Stock Simulator API",
        default_version='v1',
        description="API for retrieving stock prices",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('stocks.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.json/', schema_view.without_ui(cache_timeout=0), name='swagger-json'),
    path('swagger-new/', swagger_views.swagger_json_view, name='swagger-json'),
]