from django.urls import path, re_path
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from stock.views.stock_views import FetchStockDataView, StockListView, StockDetailView
from stock.openapi.schema import FETCH_STOCK_API, STOCK_LIST_API, STOCK_DETAIL_API
from user.openapi.info import openapi_info  # Reuse existing openapi_info

schema_view = get_schema_view(
    openapi_info,
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    re_path(r'^stock/swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='stock-schema-json'),
    re_path(r'^stock/swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='stock-schema-swagger-ui'),
    re_path(r'^stock/redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='stock-schema-redoc'),

    path('stocks/fetch/', FetchStockDataView.as_view(), name='fetch-stock-data'),
    path('stocks/', StockListView.as_view(), name='stock-list'),
    path('stocks/<int:stock_id>/', StockDetailView.as_view(), name='stock-detail'),
]