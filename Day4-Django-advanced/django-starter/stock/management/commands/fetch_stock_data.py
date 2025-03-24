from django.core.management.base import BaseCommand
from stock.services.stock_service import StockService
from datetime import datetime

class Command(BaseCommand):
    help = "Fetch and update stock data"

    def handle(self, *args, **options):
        self.stdout.write(f"Cron job started at: {datetime.now()}")
        result = StockService.fetch_and_update_stock_data()
        if isinstance(result, bool):
            self.stdout.write(self.style.SUCCESS("Stock data updated successfully"))
        else:
            self.stdout.write(self.style.ERROR(f"Failed to update stock data: {result}"))