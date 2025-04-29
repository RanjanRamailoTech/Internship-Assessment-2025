from django.urls import path, re_path
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from stock.views.stock_views import FetchStockDataView, StockListView, StockDetailView
from user.views.user_views import CreateUserView, LoginView, VerifyEmailView

urlpatterns = [
    path('register/', CreateUserView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('verify-email/', VerifyEmailView.as_view(), name='verifyemail'),
]