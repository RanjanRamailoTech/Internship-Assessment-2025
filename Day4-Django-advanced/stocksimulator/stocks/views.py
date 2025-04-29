from rest_framework.views import APIView
from rest_framework.response import Response
from .models import StockPrice
from .serializers import StockPriceSerializer
from django.utils import timezone
import pytz
from drf_yasg.utils import swagger_auto_schema
from .schema import stock_price_api_responses

class StockPriceAPIView(APIView):
    @swagger_auto_schema(
        operation_description="Retrieve current stock prices for all companies based on the sequence calculated from March 20, 2025.",
        responses=stock_price_api_responses  # Use the imported schema
    )
    def get(self, request):
        start_time = timezone.datetime(2025, 3, 20, 0, 0, 0, tzinfo=pytz.utc)
        current_time = timezone.now()
        time_elapsed = current_time - start_time
        minutes_elapsed = time_elapsed.total_seconds() // 60
        current_sequence = int(minutes_elapsed // 15)

        stock_prices = StockPrice.objects.filter(sequence=current_sequence)
        if not stock_prices.exists():
            return Response({"message": "No data available for this time"}, status=404)

        serializer = StockPriceSerializer(stock_prices, many=True)
        return Response(serializer.data)