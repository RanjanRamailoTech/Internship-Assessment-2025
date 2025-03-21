from django.urls import path, re_path
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from user.views.user_views import CreateUserView, LoginView, VerifyEmailView
from user.openapi.info import openapi_info  # We'll define this next

schema_view = get_schema_view(
    openapi_info,
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # Swagger and Redoc
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # User API Endpoints
    path('create/', CreateUserView.as_view(), name='create-user'),
    path('login/', LoginView.as_view(), name='login'),
    path('verify-email/<str:token>/', VerifyEmailView.as_view(), name='verify-email'),
]