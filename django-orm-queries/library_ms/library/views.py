from django.http import JsonResponse 
from django.views.decorators.csrf import csrf_exempt 
from django.views.decorators.http import require_POST 
import json 
from .models import Author, Book 
from datetime import datetime

@csrf_exempt 
@require_POST 
def populate_data(request): 
    try: 
        data = json.loads(request.body) 
        author_data = data.get('author') 
        books_data = data.get('books', [])
    
            # Create or get author
        author, _ = Author.objects.get_or_create(
            full_name=author_data['full_name'],
            defaults={'birth_year': author_data['birth_year']}
        )

        # Create books
        books = [
            Book(
                title=book['title'],
                published_on=datetime.strptime(book['published_on'], '%Y-%m-%d').date(),
                author=author
            )
            for book in books_data
        ]
        Book.objects.bulk_create(books)

        return JsonResponse({'status': 'success', 'message': f'Created {len(books)} books for {author.full_name}'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)