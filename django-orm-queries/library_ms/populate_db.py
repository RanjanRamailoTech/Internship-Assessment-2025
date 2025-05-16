import os
import django
import random
from datetime import datetime, date
from faker import Faker
from django.db import transaction

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_ms.settings')
django.setup()

from library.models import Author, Book, Profile, Category

def generate_bulk_data(num_authors=10, total_books=30, num_categories=5):
    fake = Faker()
    authors = []
    profiles = []
    books = []
    categories = []

    print(f"Generating {num_categories} categories...")
    for _ in range(num_categories):
        categories.append(Category(name=fake.word().capitalize()))
    try:
        with transaction.atomic():
            Category.objects.bulk_create(categories)
            print(f"Created {len(categories)} categories")
    except Exception as e:
        print(f"Error creating categories: {e}")
        return

    print(f"Generating {num_authors} authors and profiles...")
    for _ in range(num_authors):
        author = Author(
            full_name=fake.name(),
            birth_year=random.randint(1900, 2000)  # Authors born between 1900-2000
        )
        authors.append(author)
        profiles.append(Profile(
            author=author,
            bio=fake.paragraph(),
            website=fake.url()
        ))

    try:
        with transaction.atomic():
            Author.objects.bulk_create(authors)
            Profile.objects.bulk_create(profiles)
            print(f"Created {len(authors)} authors and {len(profiles)} profiles")
    except Exception as e:
        print(f"Error creating authors/profiles: {e}")
        return

    print(f"Generating {total_books} books...")
    category_list = list(Category.objects.all())
    author_list = list(Author.objects.all())
    
    for _ in range(total_books):
        author = random.choice(author_list)
        # Ensure book is published when author is at least 15 years old
        min_pub_year = author.birth_year + 15
        max_pub_year = 2025
        # If author is too young (born after 2010), skip and pick another author
        if min_pub_year > max_pub_year:
            continue
            
        published_year = random.randint(min_pub_year, max_pub_year)
        start_date = date(published_year, 1, 1)
        end_date = date(published_year, 12, 31)
        published_date = fake.date_between(start_date=start_date, end_date=end_date)
        
        book = Book(
            title=fake.sentence(nb_words=random.randint(3, 8))[:255],
            published_on=published_date,
            author=author,
            is_modern=published_year > 2000
        )
        books.append((book, random.sample(category_list, k=random.randint(1, 3))))

    try:
        with transaction.atomic():
            Book.objects.bulk_create([b[0] for b in books])
            for book, cats in books:
                book.categories.set(cats)
            print(f"Created {len(books)} books with categories")
    except Exception as e:
        print(f"Error creating books: {e}")
        return

if __name__ == '__main__':
    generate_bulk_data()