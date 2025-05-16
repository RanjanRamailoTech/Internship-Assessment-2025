import requests
from shared.helpers.logging_helper import logger

class StockAccessor:
    STOCK_DATA_URL = "http://127.0.0.1:8000/api/stock-prices/"

    @staticmethod
    def fetch_stock_data():
        try:
            response = requests.get(StockAccessor.STOCK_DATA_URL)
            response.raise_for_status()
            stock_data = response.json()  #format: [{"company_name": "ABC", "current_price": 123.45}, ...]
            logger.info(f"Stock data fetched successfully: {stock_data}")
            return stock_data
        except requests.RequestException as e:
            logger.error(f"Failed to fetch stock data: {e}")
            return None