import csv
import random
from faker import Faker
from datetime import datetime, date

fake = Faker()

def generate_books_seed_csv(filename='data/books_seed.csv', num_rows=30):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['title', 'published_on', 'author_name', 'birth_year'])
        for _ in range(num_rows):
            published_year = random.randint(1900, 2025)
            start_date = date(published_year, 1, 1)
            end_date = date(published_year, 12, 31)
            published_date = fake.date_between(start_date=start_date, end_date=end_date)
            writer.writerow([
                fake.sentence(nb_words=random.randint(3, 8))[:255],
                published_date.strftime('%Y-%m-%d'),
                fake.name(),
                random.randint(1900, 2000)
            ])
    print(f"Created {filename} with {num_rows} rows")

def generate_temp_books_csv(filename='data/temp_books.csv', num_rows=10):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['title', 'published_on', 'author_name', 'birth_year'])
        for _ in range(num_rows):
            published_year = random.randint(1900, 2025)
            start_date = date(published_year, 1, 1)
            end_date = date(published_year, 12, 31)
            published_date = fake.date_between(start_date=start_date, end_date=end_date)
            writer.writerow([
                f"Temporary {fake.sentence(nb_words=3)}"[:255],
                published_date.strftime('%Y-%m-%d'),
                fake.name(),
                random.randint(1900, 2000)
            ])
    print(f"Created {filename} with {num_rows} rows")

def generate_large_books_csv(filename='data/large_books.csv', num_rows=50000):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['title', 'published_on', 'author_name', 'birth_year'])
        for _ in range(num_rows):
            published_year = random.randint(1900, 2025)
            start_date = date(published_year, 1, 1)
            end_date = date(published_year, 12, 31)
            published_date = fake.date_between(start_date=start_date, end_date=end_date)
            writer.writerow([
                fake.sentence(nb_words=random.randint(3, 8))[:255],
                published_date.strftime('%Y-%m-%d'),
                fake.name(),
                random.randint(1900, 2000)
            ])
    print(f"Created {filename} with {num_rows} rows")

if __name__ == '__main__':
    import os
    os.makedirs('data', exist_ok=True)
    generate_books_seed_csv()
    generate_temp_books_csv()
    generate_large_books_csv()