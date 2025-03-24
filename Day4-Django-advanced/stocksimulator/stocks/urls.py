from django.urls import path
from .views import StockPriceAPIView

urlpatterns = [
    path('api/stock-prices/', StockPriceAPIView.as_view(), name='stock-prices'),
]