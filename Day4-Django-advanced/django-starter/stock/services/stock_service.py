from django.core.cache import cache
from stock.models.stock import Stock
from stock.accessors.stock_accessor import StockAccessor
from stock.serializers.stock_serializer import StockSerializer
from shared.helpers.logging_helper import logger

class StockService:
    @staticmethod
    def fetch_and_update_stock_data():
        logger.info("Fetching stock data...")
        stock_data = StockAccessor.fetch_stock_data()
        if stock_data is None:
            logger.error("Stock data fetch returned None")
            return "Failed to fetch stock data"
        
        logger.info(f"Stock data received: {stock_data}")
        for data in stock_data:
            # Use company_name as the lookup field, update current_price
            Stock.objects.update_or_create(
                company_name=data["company"],  # Lookup by company_name
                defaults={"current_price": data["price"]}  # Update this field
            )
        
        cache.delete("stock_list")
        logger.info("Stock data updated and cache cleared")
        return True
    
    @staticmethod
    def get_all_stocks():
        cached_stocks = cache.get("stock_list")
        if cached_stocks is not None:
            return cached_stocks

        stocks = Stock.objects.all()
        serialized_stocks = StockSerializer(stocks, many=True).data
        cache.set("stock_list", serialized_stocks, timeout=15 * 60)  # 15 minutes
        return serialized_stocks

    @staticmethod
    def get_stock_detail(stock_id):
        stock = Stock.objects.filter(id=stock_id).first()
        if stock:
            return StockSerializer(stock).data
        return None