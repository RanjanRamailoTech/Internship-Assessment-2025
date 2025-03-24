from django.urls import path
from stock.views.stock_views import FetchStockDataView, StockListView, StockDetailView

urlpatterns = [
    path('fetch/', FetchStockDataView.as_view(), name='fetch-stock-data'),
    path('', StockListView.as_view(), name='stock-list'),
    path('<int:stock_id>/', StockDetailView.as_view(), name='stock-detail'),
]