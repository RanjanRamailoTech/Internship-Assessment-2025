import csv
from django.core.management.base import BaseCommand
from stocks.models import Company, StockPrice
from django.db import transaction

class Command(BaseCommand):
    help = 'Import stock prices from CSV file'

    def handle(self, *args, **kwargs):
        file_path = 'stocks/stock_prices.csv'
        
        # Wrap everything in a single transaction to reduce overhead
        with transaction.atomic():
            # Step 1: Create or get all companies
            with open(file_path, 'r') as file:
                reader = csv.reader(file)
                companies = next(reader)  # First row is company names
                
                # Bulk create companies if they don’t exist
                existing_companies = {c.name: c for c in Company.objects.all()}
                new_companies = [Company(name=name) for name in companies if name not in existing_companies]
                if new_companies:
                    Company.objects.bulk_create(new_companies)
                
                # Fetch all companies into memory
                company_map = {c.name: c for c in Company.objects.all()}

            # Step 2: Prepare stock price objects in batches
            batch_size = 1000  # Adjust based on your system’s memory
            stock_prices = []
            
            with open(file_path, 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header row
                for sequence, row in enumerate(reader):
                    for i, price in enumerate(row):
                        stock_prices.append(
                            StockPrice(
                                company=company_map[companies[i]],
                                price=float(price),
                                sequence=sequence
                            )
                        )
                    
                    # Bulk create when batch size is reached
                    if len(stock_prices) >= batch_size:
                        StockPrice.objects.bulk_create(stock_prices)
                        stock_prices = []
                        self.stdout.write(self.style.SUCCESS(f'Imported up to sequence {sequence}'))

            # Insert any remaining stock prices
            if stock_prices:
                StockPrice.objects.bulk_create(stock_prices)

        self.stdout.write(self.style.SUCCESS('Successfully imported all stock data'))