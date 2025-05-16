from django.urls import path, re_path
from drf_yasg.views import get_schema_view
from rest_framework import permissions
import stock.views.stock_views as stock_views

urlpatterns = [
    path('stocks/fetch/', stock_views.FetchStockDataView.as_view(), name='fetch-stock-data'),
    path('stocks/', stock_views.StockListView.as_view(), name='stock-list'),
    path('stocks/<int:stock_id>/', stock_views.StockDetailView.as_view(), name='stock-detail'),
]