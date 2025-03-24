from rest_framework.views import APIView
from ramailo.builders.response_builder import ResponseBuilder
from stock.services.stock_service import StockService
from stock.openapi.schema import FETCH_STOCK_API, STOCK_LIST_API, STOCK_DETAIL_API
from drf_yasg.utils import swagger_auto_schema

class FetchStockDataView(APIView):
    @swagger_auto_schema(**FETCH_STOCK_API)
    def post(self, request):
        result = StockService.fetch_and_update_stock_data()
        if isinstance(result, bool):
            return ResponseBuilder().created_201().result_object({"data": {"message": "Stock data updated"}}).get_response()
        return ResponseBuilder().internal_error_500().result_object({"data": {"message": result}}).get_response()

class StockListView(APIView):
    @swagger_auto_schema(**STOCK_LIST_API)
    def get(self, request):
        stocks = StockService.get_all_stocks()
        return ResponseBuilder().ok_200().result_object({"data": stocks}).get_response()

class StockDetailView(APIView):
    @swagger_auto_schema(**STOCK_DETAIL_API)
    def get(self, request, stock_id):
        stock = StockService.get_stock_detail(stock_id)
        if stock:
            return ResponseBuilder().ok_200().result_object({"data": stock}).get_response()
        return ResponseBuilder().not_found_404().result_object({"data": {"message": "Stock not found"}}).get_response()