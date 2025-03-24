from rest_framework.views import APIView
from rest_framework.response import Response
from .models import StockPrice
from .serializers import StockPriceSerializer
from django.utils import timezone
import pytz

class StockPriceAPIView(APIView):
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