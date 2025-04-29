from drf_yasg import openapi

openapi_info = openapi.Info(
    title="User API",
    default_version='v1',
    description="API for user management including creation, login, and email verification.",
    terms_of_service="https://www.example.com/terms/",
    contact=openapi.Contact(email="support@example.com"),
    license=openapi.License(name="MIT License"),
)