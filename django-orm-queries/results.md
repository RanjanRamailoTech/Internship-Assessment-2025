# Project setup
Write about project setup, models, and the pupulating scripts, File scructure


# Django ORM

## Part A  Warm‑up

### 1. Print all author names in reverse alphabetical order.
```
>>> Author.objects.order_by('-full_name').values_list('full_name', flat=True)
<QuerySet ['Steven Bryan', 'Linda Pollard', 'Joseph Gutierrez', 'Joseph Clark', 'John Fowler', 'Jennifer Smith', 'Jason Price', 'Dana Jacobs', 'Christopher Quinn', 'Charles Escobar']>
```

### 2. Show only id & title of books published after 2000.
```
>>> Book.objects.filter(published_on__year__gt=2000).values('id', 'title')
<QuerySet [{'id': 12, 'title': 'Relate police since detail trial bill cold.'}, {'id': 10, 'title': 'Fill who adult rule.'}, {'id': 15, 'title': 'Vote sure source drive image travel.'}, {'id': 20, 'title': 'Interest time risk station.'}, {'id': 30, 'title': 'Still wide support enjoy because.'}, {'id': 8, 'title': 'System all term success.'}, {'id': 26, 'title': 'Truth perform owner argue.'}, {'id': 25, 'title': 'Our sense successful.'}, {'id': 17, 'title': 'Trip several newspaper that.'}, {'id': 13, 'title': 'Majority should station culture.'}]>
```

## Part B  Aggregations & Filtering
### 1. Rich get richer – author(s) with the highest average publication year ((author, avg_year), top 3).
```
>>> from django.db.models import Avg
>>> 
>>> Author.objects.annotate(
...     avg_pub_year=Avg('books__published_on__year')
... ).order_by('-avg_pub_year')[:3].values('full_name', 'avg_pub_year')
<QuerySet [{'full_name': 'Jennifer Smith', 'avg_pub_year': 2005.25}, {'full_name': 'Christopher Quinn', 'avg_pub_year': 2002.75}, {'full_name': 'Charles Escobar', 'avg_pub_year': 2002.0}]>
```

### 2. Sparse authors – authors with ≤ 2 books.
```
>>> from django.db.models import Count
>>> 
>>> Author.objects.annotate(
...     book_count=Count('books')
... ).filter(book_count__lte=2).values('full_name', 'book_count')
<QuerySet [{'full_name': 'John Fowler', 'book_count': 2}, {'full_name': 'Steven Bryan', 'book_count': 1}, {'full_name': 'Jason Price', 'book_count': 1}, {'full_name': 'Charles Escobar', 'book_count': 2}, {'full_name': 'Joseph Clark', 'book_count': 2}]>
```

### 3. Longest titles – five longest book titles with their character counts.
```
>>> from django.db.models.functions import Length
>>> Book.objects.annotate(
...     title_length=Length('title')
... ).order_by('-title_length')[:5].values('title', 'title_length')
<QuerySet [{'title': 'Reality outside who civil heavy page visit large.', 'title_length': 49}, {'title': 'Professional say save who unit technology huge.', 'title_length': 47}, {'title': 'What less begin character marriage which word.', 'title_length': 46}, {'title': 'Indeed professor laugh Congress seven give.', 'title_length': 43}, {'title': 'Relate police since detail trial bill cold.', 'title_length': 43}]>
```

### 4. Year gaps – detect gaps ≥ 15 years between successive books by the same author and print a descriptive line.
```
>>> from django.db.models import Window, F
>>> from django.db.models.functions import ExtractYear
>>> from django.db.models.functions import Lag
>>> books = Book.objects.annotate(
...     pub_year=ExtractYear('published_on'),
...     prev_pub_year=Window(
...         expression=Lag('published_on__year'),
...         partition_by=[F('author')],
...         order_by=F('published_on').asc()
...     )
... ).filter(
...     pub_year__gte=F('prev_pub_year') + 15
... ).order_by('author', 'published_on')
>>> 
>>> for book in books:
...     print(f"Author {book.author.full_name} had a {book.pub_year - book.prev_pub_year}-year gap between books (from {book.prev_pub_year} to {book.pub_year})")
... 
Author Charles Escobar had a 16-year gap between books (from 1994 to 2010)
Author Joseph Clark had a 16-year gap between books (from 1990 to 2006)
Author Christopher Quinn had a 31-year gap between books (from 1988 to 2019)
Author Joseph Gutierrez had a 18-year gap between books (from 1971 to 1989)
Author Joseph Gutierrez had a 23-year gap between books (from 1989 to 2012)
Author John Fowler had a 27-year gap between books (from 1940 to 1967)
Author Linda Pollard had a 22-year gap between books (from 1958 to 1980)
Author Linda Pollard had a 27-year gap between books (from 1990 to 2017)
>>> 
```


## Part C Relationships & Joins
### 1. Books with Author Age
 For every book, return a tuple of (title, author_age_at_publication), where author_age_at_publication = published_on.year − birth_year.

```
>>> from django.db.models import F, ExpressionWrapper, fields
>>> 
>>> Book.objects.annotate(
...     author_age=ExpressionWrapper(
...         F('published_on__year') - F('author__birth_year'),
...         output_field=fields.IntegerField()
...     )
... ).values('title', 'author_age')
<QuerySet [{'title': 'Congress sister sing so team difference.', 'author_age': 62}, {'title': 'Part speak south plant blue.', 'author_age': 30}, {'title': 'Entire receive event seem manage.', 'author_age': 16}, {'title': 'Life material worry on.', 'author_age': 35}, {'title': 'Indeed professor laugh Congress seven give.', 'author_age': 57}, {'title': 'At others personal unit animal mind along.', 'author_age': 25}, {'title': 'What less begin character marriage which word.', 'author_age': 34}, {'title': 'System all term success.', 'author_age': 53}, {'title': 'Head outside part maintain ago until ten.', 'author_age': 24}, {'title': 'Fill who adult rule.', 'author_age': 66}, {'title': 'Claim front agent.', 'author_age': 25}, {'title': 'Relate police since detail trial bill cold.', 'author_age': 42}, {'title': 'Majority should station culture.', 'author_age': 60}, {'title': 'Reality outside who civil heavy page visit large.', 'author_age': 23}, {'title': 'Vote sure source drive image travel.', 'author_age': 42}, {'title': 'Citizen born not.', 'author_age': 50}, {'title': 'Trip several newspaper that.', 'author_age': 56}, {'title': 'Professional say save who unit technology huge.', 'author_age': 32}, {'title': 'Standard first.', 'author_age': 25}, {'title': 'Interest time risk station.', 'author_age': 79}, '...(remaining elements truncated)...']>
>>> 
```

### 2. Authors & Their First Book
 List each author alongside the title and year of their earliest-published book.
```
>>> from django.db.models import Min, Subquery, OuterRef
>>> 
>>> first_books = Book.objects.filter(
...     author=OuterRef('pk')
... ).order_by('published_on')[:1]
>>> 
>>> Author.objects.annotate(
...     first_book_title=Subquery(first_books.values('title')),
...     first_book_year=Subquery(first_books.values('published_on__year'))
... ).values('full_name', 'first_book_title', 'first_book_year')
<QuerySet [{'full_name': 'Jennifer Smith', 'first_book_title': 'Reduce Democrat still allow right.', 'first_book_year': 1991}, {'full_name': 'Charles Escobar', 'first_book_title': 'Run energy little be bring meeting.', 'first_book_year': 1994}, {'full_name': 'Joseph Clark', 'first_book_title': 'Citizen born not.', 'first_book_year': 1990}, {'full_name': 'Christopher Quinn', 'first_book_title': 'Girl fear.', 'first_book_year': 1981}, {'full_name': 'Steven Bryan', 'first_book_title': 'Reality outside who civil heavy page visit large.', 'first_book_year': 1930}, {'full_name': 'Joseph Gutierrez', 'first_book_title': 'Entire receive event seem manage.', 'first_book_year': 1971}, {'full_name': 'Jason Price', 'first_book_title': 'Between new sort budget.', 'first_book_year': 1979}, {'full_name': 'John Fowler', 'first_book_title': 'Life material worry on.', 'first_book_year': 1940}, {'full_name': 'Dana Jacobs', 'first_book_title': 'Standard first.', 'first_book_year': 1992}, {'full_name': 'Linda Pollard', 'first_book_title': 'Soldier ten modern move real behind series.', 'first_book_year': 1955}]>
>>> 
```

### 3. Prolific Since 2000
 Retrieve all authors who have written more than 3 books published after January 1, 2000.
```
>>> from django.db.models import Count
>>> 
>>> Author.objects.filter(
...     books__published_on__year__gt=2000
... ).annotate(
...     recent_books=Count('books')
... ).filter(
...     recent_books__gt=3
... ).values('full_name', 'recent_books')
<QuerySet []>
>>> 
```

### 4. Books by Young Authors
 Find all books where the author was under 30 when they published it.
```
>>> Book.objects.annotate(
...     author_age=F('published_on__year') - F('author__birth_year')
... ).filter(
...     author_age__lt=30
... ).values('title', 'author__full_name', 'author_age')
<QuerySet [{'title': 'Entire receive event seem manage.', 'author__full_name': 'Joseph Gutierrez', 'author_age': 16}, {'title': 'At others personal unit animal mind along.', 'author__full_name': 'Christopher Quinn', 'author_age': 25}, {'title': 'Head outside part maintain ago until ten.', 'author__full_name': 'Linda Pollard', 'author_age': 24}, {'title': 'Claim front agent.', 'author__full_name': 'Linda Pollard', 'author_age': 25}, {'title': 'Reality outside who civil heavy page visit large.', 'author__full_name': 'Steven Bryan', 'author_age': 23}, {'title': 'Standard first.', 'author__full_name': 'Dana Jacobs', 'author_age': 25}, {'title': 'Girl fear.', 'author__full_name': 'Christopher Quinn', 'author_age': 18}, {'title': 'Former hair.', 'author__full_name': 'Joseph Gutierrez', 'author_age': 16}, {'title': 'Soldier ten modern move real behind series.', 'author__full_name': 'Linda Pollard', 'author_age': 22}]>
>>> 

```

### 5. Title Search Joins
 Return all authors who have at least one book with "Django" (case-insensitive) in its title.
```
>>> Author.objects.filter(
...     books__title__icontains='django'
... ).distinct().values('full_name')
<QuerySet []>
>>> 
>>> Author.objects.filter(
...     books__title__icontains='woman'
... ).distinct().values('full_name')
<QuerySet []>
>>> 
>>> Author.objects.filter(
...     books__title__icontains='technology'
... ).distinct().values('full_name')
<QuerySet [{'full_name': 'Dana Jacobs'}]>
>>> 
>>> Author.objects.filter(
...     books__title__icontains='Technology'
... ).distinct().values('full_name')
<QuerySet [{'full_name': 'Dana Jacobs'}]>
>>> 
```

## Part D Data Modification & Transactions
### 1. Bulk Birth-Year Update
 Increment the birth_year by 1 for every author who has no books.
```
>>> from django.db.models import Count
>>> 
>>> Author.objects.annotate(book_count=Count('books')).filter(book_count=0).update(birth_year=F('birth_year') + 1)
0
>>> 
```

### 2. Delete Ancient Books
 Delete all Book records published before January 1, 1900.
```
>>> from datetime import date
>>> 
>>> Book.objects.filter(published_on__lt=date(1900, 1, 1)).delete()
(0, {})
```

### 3. Atomic Creation
 In a single transaction, create a new author and three associated books. If any part fails, rollback everything.

```
>>> from django.db import transaction
>>> 
>>> try:
...     with transaction.atomic():
...         new_author = Author.objects.create(
...             full_name="J.K. Rowling",
...             birth_year=1965
...         )
...         Book.objects.bulk_create([
...             Book(title="Harry Potter 1", published_on=date(1997, 6, 26), author=new_author),
...             Book(title="Harry Potter 2", published_on=date(1998, 7, 2), author=new_author),
...             Book(title="Harry Potter 3", published_on=date(1999, 7, 8), author=new_author)
...         ])
... except Exception as e:
...     print(f"Transaction failed: {e}")
... 
[<Book: Harry Potter 1>, <Book: Harry Potter 2>, <Book: Harry Potter 3>]
>>> 
```

### 4. Title Normalization
 Convert to uppercase the title of every book whose length is less than 10 characters.
```
>>> from django.db.models.functions import Length, Upper
>>> Book.objects.annotate(title_len=Length('title')).filter(title_len__lt=10).update(title=Upper('title'))
0
>>> Book.objects.annotate(title_len=Length('title')).filter(title_len__lt=15).update(title=Upper('title'))
5
>>> 
```

## Part E  N + 1 Detective 
### 1. Build a naïve loop printing "<title> – <author>"; measure SQL count.
```
>>> from django.db import connection
>>> 
>>> connection.queries_log.clear()
>>> books = Book.objects.all()
>>> for book in books:
...     print(f"{book.title} - {book.author.full_name}")
... 
Congress sister sing so team difference. - John Fowler
Part speak south plant blue. - Dana Jacobs
Entire receive event seem manage. - Joseph Gutierrez
Life material worry on. - John Fowler
Indeed professor laugh Congress seven give. - Linda Pollard
At others personal unit animal mind along. - Christopher Quinn
What less begin character marriage which word. - Joseph Gutierrez
System all term success. - Jennifer Smith
Head outside part maintain ago until ten. - Linda Pollard
Fill who adult rule. - Joseph Clark
Claim front agent. - Linda Pollard
Relate police since detail trial bill cold. - Jennifer Smith
Majority should station culture. - Christopher Quinn
Reality outside who civil heavy page visit large. - Steven Bryan
Vote sure source drive image travel. - Dana Jacobs
Citizen born not. - Joseph Clark
Trip several newspaper that. - Christopher Quinn
Professional say save who unit technology huge. - Dana Jacobs
Standard first. - Dana Jacobs
Interest time risk station. - Charles Escobar
Run energy little be bring meeting. - Charles Escobar
GIRL FEAR. - Christopher Quinn
FORMER HAIR. - Joseph Gutierrez
Soldier ten modern move real behind series. - Linda Pollard
Our sense successful. - Linda Pollard
Truth perform owner argue. - Jennifer Smith
Into enter recognize something fish movie. - Linda Pollard
Reduce Democrat still allow right. - Jennifer Smith
Between new sort budget. - Jason Price
Still wide support enjoy because. - Joseph Gutierrez
HARRY POTTER 1 - J.K. Rowling
HARRY POTTER 2 - J.K. Rowling
HARRY POTTER 3 - J.K. Rowling
>>> print(f"SQL queries: {len(connection.queries)}")
SQL queries: 34
>>> 
```
**Here Total sql query count is 34**

### 2. Optimise using select_related('author'); compare counts.
```
>>> connection.queries_log.clear()
>>> books = Book.objects.select_related('author').all()
>>> for book in books:
...     print(f"{book.title} - {book.author.full_name}")
... 
Congress sister sing so team difference. - John Fowler
Part speak south plant blue. - Dana Jacobs
Entire receive event seem manage. - Joseph Gutierrez
Life material worry on. - John Fowler
Indeed professor laugh Congress seven give. - Linda Pollard
At others personal unit animal mind along. - Christopher Quinn
What less begin character marriage which word. - Joseph Gutierrez
System all term success. - Jennifer Smith
Head outside part maintain ago until ten. - Linda Pollard
Fill who adult rule. - Joseph Clark
Claim front agent. - Linda Pollard
Relate police since detail trial bill cold. - Jennifer Smith
Majority should station culture. - Christopher Quinn
Reality outside who civil heavy page visit large. - Steven Bryan
Vote sure source drive image travel. - Dana Jacobs
Citizen born not. - Joseph Clark
Trip several newspaper that. - Christopher Quinn
Professional say save who unit technology huge. - Dana Jacobs
Standard first. - Dana Jacobs
Interest time risk station. - Charles Escobar
Run energy little be bring meeting. - Charles Escobar
GIRL FEAR. - Christopher Quinn
FORMER HAIR. - Joseph Gutierrez
Soldier ten modern move real behind series. - Linda Pollard
Our sense successful. - Linda Pollard
Truth perform owner argue. - Jennifer Smith
Into enter recognize something fish movie. - Linda Pollard
Reduce Democrat still allow right. - Jennifer Smith
Between new sort budget. - Jason Price
Still wide support enjoy because. - Joseph Gutierrez
HARRY POTTER 1 - J.K. Rowling
HARRY POTTER 2 - J.K. Rowling
HARRY POTTER 3 - J.K. Rowling
>>> print(f"SQL queries: {len(connection.queries)}")
SQL queries: 1
>>> 
```
**Using `select_related`: Total sql query count is 1**

### 3. Repeat for author → list of books: naïve vs prefetch_related('books').
```
>>> connection.queries_log.clear()
>>> authors = Author.objects.all()
>>> for author in authors:
...     print(f"{author.full_name}: {[b.title for b in author.books.all()]}")
... 
Jennifer Smith: ['System all term success.', 'Relate police since detail trial bill cold.', 'Truth perform owner argue.', 'Reduce Democrat still allow right.']
Charles Escobar: ['Interest time risk station.', 'Run energy little be bring meeting.']
Joseph Clark: ['Fill who adult rule.', 'Citizen born not.']
Christopher Quinn: ['At others personal unit animal mind along.', 'Majority should station culture.', 'Trip several newspaper that.', 'GIRL FEAR.']
Steven Bryan: ['Reality outside who civil heavy page visit large.']
Joseph Gutierrez: ['Entire receive event seem manage.', 'What less begin character marriage which word.', 'FORMER HAIR.', 'Still wide support enjoy because.']
Jason Price: ['Between new sort budget.']
John Fowler: ['Congress sister sing so team difference.', 'Life material worry on.']
Dana Jacobs: ['Part speak south plant blue.', 'Vote sure source drive image travel.', 'Professional say save who unit technology huge.', 'Standard first.']
Linda Pollard: ['Indeed professor laugh Congress seven give.', 'Head outside part maintain ago until ten.', 'Claim front agent.', 'Soldier ten modern move real behind series.', 'Our sense successful.', 'Into enter recognize something fish movie.']
J.K. Rowling: ['HARRY POTTER 1', 'HARRY POTTER 2', 'HARRY POTTER 3']
>>> print(f"SQL queries: {len(connection.queries)}")
SQL queries: 12
>>> 
>>> connection.queries_log.clear()
>>> authors = Author.objects.prefetch_related('books').all()
>>> for author in authors:
...     print(f"{author.full_name}: {[b.title for b in author.books.all()]}")
... 
Jennifer Smith: ['System all term success.', 'Relate police since detail trial bill cold.', 'Truth perform owner argue.', 'Reduce Democrat still allow right.']
Charles Escobar: ['Interest time risk station.', 'Run energy little be bring meeting.']
Joseph Clark: ['Fill who adult rule.', 'Citizen born not.']
Christopher Quinn: ['At others personal unit animal mind along.', 'Majority should station culture.', 'Trip several newspaper that.', 'GIRL FEAR.']
Steven Bryan: ['Reality outside who civil heavy page visit large.']
Joseph Gutierrez: ['Entire receive event seem manage.', 'What less begin character marriage which word.', 'FORMER HAIR.', 'Still wide support enjoy because.']
Jason Price: ['Between new sort budget.']
John Fowler: ['Congress sister sing so team difference.', 'Life material worry on.']
Dana Jacobs: ['Part speak south plant blue.', 'Vote sure source drive image travel.', 'Professional say save who unit technology huge.', 'Standard first.']
Linda Pollard: ['Indeed professor laugh Congress seven give.', 'Head outside part maintain ago until ten.', 'Claim front agent.', 'Soldier ten modern move real behind series.', 'Our sense successful.', 'Into enter recognize something fish movie.']
J.K. Rowling: ['HARRY POTTER 1', 'HARRY POTTER 2', 'HARRY POTTER 3']
>>> print(f"SQL queries: {len(connection.queries)}")
SQL queries: 2
```
**Using naive approach: Total sql query count is 12**
**Using prefetch_related: Total sql query count is 2**

### 4. How many SQL statements are executed?list(Book.objects.only("title")) after a cold reset.
```
>>> from django.db import connection
>>> connection.queries_log.clear()
>>> 
>>> # Execute the query
>>> books = list(Book.objects.only("title"))
>>> print(len(connection.queries))
1
>>> print(connection.queries[0]['sql'])
SELECT "library_book"."id", "library_book"."title" FROM "library_book"
>>> 
```
**SQL Statements executed: 1**

### 5. Will calling .exists() on an already‑evaluated queryset hit the DB again?
```
>>> connection.queries_log.clear()
>>> books = Book.objects.all()
>>> list(books)
[<Book: Congress sister sing so team difference.>, <Book: Part speak south plant blue.>, <Book: Entire receive event seem manage.>, <Book: Life material worry on.>, <Book: Indeed professor laugh Congress seven give.>, <Book: At others personal unit animal mind along.>, <Book: What less begin character marriage which word.>, <Book: System all term success.>, <Book: Head outside part maintain ago until ten.>, <Book: Fill who adult rule.>, <Book: Claim front agent.>, <Book: Relate police since detail trial bill cold.>, <Book: Majority should station culture.>, <Book: Reality outside who civil heavy page visit large.>, <Book: Vote sure source drive image travel.>, <Book: Citizen born not.>, <Book: Trip several newspaper that.>, <Book: Professional say save who unit technology huge.>, <Book: Standard first.>, <Book: Interest time risk station.>, <Book: Run energy little be bring meeting.>, <Book: GIRL FEAR.>, <Book: FORMER HAIR.>, <Book: Soldier ten modern move real behind series.>, <Book: Our sense successful.>, <Book: Truth perform owner argue.>, <Book: Into enter recognize something fish movie.>, <Book: Reduce Democrat still allow right.>, <Book: Between new sort budget.>, <Book: Still wide support enjoy because.>, <Book: HARRY POTTER 1>, <Book: HARRY POTTER 2>, <Book: HARRY POTTER 3>]
>>> print(f"Queries after evaluation: {len(connection.queries)}")
Queries after evaluation: 1
>>> 
>>> print(f"First query: {connection.queries[0]['sql']}")
First query: SELECT "library_book"."id", "library_book"."title", "library_book"."published_on", "library_book"."author_id", "library_book"."is_modern" FROM "library_book"
>>> 
>>> exists_result = books.exists()
>>> 
>>> print(f"Queries after exists(): {len(connection.queries)}")
Queries after exists(): 1
>>> 
```
**`exists()` doesnot execute any extra query**

### 6. len(Book.objects.all()) vs Book.objects.count() – which is cheaper?
```
>>> connection.queries_log.clear()
>>> 
>>> books = Book.objects.all()
>>> print(f"Using len(): {len(books)}")
Using len(): 33
>>> print(f"Query for len(): {connection.queries[-1]['sql']}")
Query for len(): SELECT "library_book"."id", "library_book"."title", "library_book"."published_on", "library_book"."author_id", "library_book"."is_modern" FROM "library_book"
>>> print(f"Time for len(): {connection.queries[-1]['time']} sec")
Time for len(): 0.000 sec
>>> 
>>> connection.queries_log.clear()
>>> print(f"Using count(): {Book.objects.count()}")
Using count(): 33
>>> print(f"Query for count(): {connection.queries[-1]['sql']}")
Query for count(): SELECT COUNT(*) AS "__count" FROM "library_book"
>>> print(f"Time for count(): {connection.queries[-1]['time']} sec")
Time for count(): 0.000 sec
>>> 
```
**Both `len` with `objects.all()` and `count()` seems to execute in `0.000 sec` because the number of data is very low (33 in total). However if we increase the data to even thousands there will be some differences. We will look into this condition later**

### 7. Identify the faster approach to fetch author names when you already have the books queryset loaded:[book.author.full_name for book in books] vs books = books.select_related("author") before looping.

- **naive approach**: book.author.full_name for book in books
```
>>> connection.queries_log.clear()
>>> books = Book.objects.all()
>>> names = [book.author.full_name for book in books]
>>> print(len(connection.queries))
34
>>> 
```
**using `select_related`**: books = books.select_related("author") before looping

```
>>> connection.queries_log.clear()
>>> 
>>> books = Book.objects.select_related("author").all()
>>> names = [book.author.full_name for book in books]
>>> print(len(connection.queries))
1
>>> 
```
**naive approach took 34 (N+1) queries to run while `selected_related` before looping took just 1 query. So the books = books.select_related("author") before looping is better and faster**

## 8. Predict query count:Author.objects.prefetch_related("books").aggregate(total=Count("books"))
```
>>> connection.queries_log.clear()
>>> Author.objects.prefetch_related('books').aggregate(total=Count('books'))
{'total': 33}
>>> print(len(connection.queries))
1
```
**Took 1 query to execute**


## Part F  Class‑Method Helpers
### 1. Add two helpers per model:
- **Author**
**oldest_author() → returns (name, birth_year) of the eldest author.**
```
    @classmethod
    def oldest_author(cls):
        return cls.objects.order_by('birth_year').first()
```
**authors_with_books_published_after(year) → list of author names**
```
    @classmethod
    def authors_with_books_published_after(cls, year):
        return cls.objects.filter(books__published_on__year__gt=year).distinct().values_list('full_name', flat=True)
```

- **Book**
**random_recommendation() → random book at SQL**
```
@classmethod
    def random_recommendation(cls):
        return cls.objects.order_by('?').first()
```
**level.bulk_mark_as_modern(year_cutoff) → bulk‑update post‑cutoff books to is_modern=True; return rows affected.**
```
    @classmethod
    def bulk_mark_as_modern(cls, year_cutoff):
        return cls.objects.filter(published_on__year__gt=year_cutoff).update(is_modern=True)
```

#### Test each helper from the shell.
**Test Author.oldest_author()**
```
>>> oldest = Author.oldest_author()
>>> print(oldest.full_name, oldest.birth_year)
John Fowler 1905
>>> 
```

**Test Author.authors_with_books_published_after(year)**
```
>>> Author.authors_with_books_published_after(2000)
<QuerySet ['Jennifer Smith', 'Joseph Clark', 'Dana Jacobs', 'Charles Escobar', 'Joseph Gutierrez', 'Linda Pollard', 'Christopher Quinn']>
>>> 
```
**Test Book.random_recommendation()**
```
>>> book = Book.random_recommendation()
>>> print(book.title)
Claim front agent.
>>> book = Book.random_recommendation()
>>> print(book.title)
Trip several newspaper that.
>>> book = Book.random_recommendation()
>>> print(book.title)
At others personal unit animal mind along.
>>> 
```

**Test Book.bulk_mark_as_modern(year_cutoff)**
```
>>> print(Book.bulk_mark_as_modern(2000))
10
>>> 
```

## Part G  Advanced Query Tricks
### 1. Conditional flagging – annotate each book with age_category (classic vs modern) using Case/When.
```
>>> from django.db import models
>>> from django.db.models import Case, When, Value
>>> 
>>> Book.objects.annotate(
...     age_category=Case(
...         When(published_on__year__lt=1950, then=Value('classic')),
...         default=Value('modern'),
...         output_field=models.CharField()
...     )
... )
<QuerySet [<Book: Congress sister sing so team difference.>, <Book: Part speak south plant blue.>, <Book: Entire receive event seem manage.>, <Book: Life material worry on.>, <Book: Indeed professor laugh Congress seven give.>, <Book: At others personal unit animal mind along.>, <Book: What less begin character marriage which word.>, <Book: System all term success.>, <Book: Head outside part maintain ago until ten.>, <Book: Fill who adult rule.>, <Book: Claim front agent.>, <Book: Relate police since detail trial bill cold.>, <Book: Majority should station culture.>, <Book: Reality outside who civil heavy page visit large.>, <Book: Vote sure source drive image travel.>, <Book: Citizen born not.>, <Book: Trip several newspaper that.>, <Book: Professional say save who unit technology huge.>, <Book: Standard first.>, <Book: Interest time risk station.>, '...(remaining elements truncated)...']>
>>> 
```


### 2. In‑DB arithmetic update – add 5 years to every author’s birth_year via F().
```
>>> from django.db.models import F
>>> 
>>> Author.objects.update(birth_year=F('birth_year') + 5)
11
>>> 
```

### 3. Case‑insensitive duplicate finder – locate titles that differ only by case.
```
>>> from django.db.models.functions import Lower
>>> 
>>> duplicates = (Book.objects.annotate(lower_title=Lower('title'))
...               .values('lower_title')
...               .annotate(count=Count('id'))
...               .filter(count__gt=1))
>>> 
>>> duplicates
<QuerySet []>
```
**NO Duplicates in DB**

### 4. Paginator practice – fetch titles for page 3 when paginating 10 per page.
```
>>> from django.core.paginator import Paginator
>>> 
>>> paginator = Paginator(Book.objects.order_by('title'), 10)
>>> page3 = paginator.page(3)
>>> titles = [book.title for book in page3]
>>> 
>>> titles
['Professional say save who unit technology huge.', 'Reality outside who civil heavy page visit large.', 'Reduce Democrat still allow right.', 'Relate police since detail trial bill cold.', 'Run energy little be bring meeting.', 'Soldier ten modern move real behind series.', 'Standard first.', 'Still wide support enjoy because.', 'System all term success.', 'Trip several newspaper that.']
>>> 
>>> page4 = paginator.page(4)
>>> titles = [book.title for book in page4]
>>> titles
['Truth perform owner argue.', 'Vote sure source drive image travel.', 'What less begin character marriage which word.']
>>> 
```

### 5. Iterator streaming – iterate over all books using .iterator(chunk_size=1000) and print row count without high memory use.
```
>>> count = 0
>>> for book in Book.objects.iterator(chunk_size=1000):
...     count += 1
... 
>>> print(f"Total books: {count}")
Total books: 33
```


## Part H  Transactions & Raw SQL
### 1. Atomic bulk insert – inside transaction.atomic(), create 1 000 dummy books; roll back if any year < 1900 sneaks in.
```
>>> from django.db import transaction
>>> 
>>> try:
...     with transaction.atomic():
...         books = [
...             Book(title=f"Book {i}", published_on=date(1900 + i % 100, 1, 1), 
...                  author=Author.objects.first())
...             for i in range(1000)
...         ]
...         Book.objects.bulk_create(books)
... except Exception as e:
...     print(f"Transaction failed: {e}")
... 
[<Book: Book 0>, <Book: Book 1>, <Book: Book 2>, <Book: Book 3>, <Book: Book 4>, <Book: Book 5>, <Book: Book 6>, <Book: Book 7>, <Book: Book 8>, <Book: Book 9>, <Book: Book 10>, <Book: ... <Book: Book 997>, <Book: Book 998>, <Book: Book 999>]
>>> 
```

### 2. Raw SQL read – with Book.objects.raw(), fetch titles where published_on year = author’s birth year + 30; show first 5.
```
>>> query = """
...     SELECT b.id, b.title
...     FROM library_book b
...     INNER JOIN library_author a ON b.author_id = a.id
...     WHERE CAST(strftime('%Y', b.published_on) AS INTEGER) = a.birth_year + 30
...     LIMIT 5
... """
>>> books = Book.objects.raw(query)
>>> for book in books:
...     print(book.title)
... 
Life material worry on.
Book 94
Book 194
Book 294
Book 394
>>> 
```


## Part I  CSV Data I/O 
For Part I we need 3 csvs before executing the tasks. To generate those csvs I have written a script `generate_seed_csvs.py`.
```
python generate_seed_csvs.py
Created data/books_seed.csv with 30 rows
Created data/temp_books.csv with 10 rows
Created data/large_books.csv with 50000 rows
```

### 1. Load data from CSV
- **CSV path: data/books_seed.csv (columns: title,published_on,author_name,birth_year).**
- **In shell, read the file (use Python csv), create or get each Author, then bulk‑create Book objects in chunks of 500.**

```
>>> import csv
>>> from datetime import datetime
>>> books = []
>>> with open('data/books_seed.csv', 'r') as f:
...     reader = csv.DictReader(f)
...     for row in reader:
...         author, _ = Author.objects.get_or_create(full_name=row['author_name'], defaults={'birth_year': int(row['birth_year'])})
...         books.append(Book(title=row['title'], published_on=datetime.strptime(row['published_on'], '%Y-%m-%d').date(), author=author))
...         if len(books) >= 500:
...             Book.objects.bulk_create(books)
...             books = []
... 
>>> if books:
...     Book.objects.bulk_create(books)
... 
[<Book: Create.>, <Book: Mother benefit cup next nothing oil.>, <Book: Sound anyone just there appear strategy either part situation.>, <Book: Light or business get.>, <Book: Stop you people.>, <Book: Drive message become.>, <Book: Sign station action world once.>, <Book: Manage choose benefit beautiful star nature knowledge.>, <Book: Cup more indicate I quality.>, <Book: Reach memory bring art whose item computer job force lot.>, <Book: If social new one you.>, <Book: Recently less population special measure high whole seem gas.>, <Book: Course your gun.>, <Book: Religious else as learn.>, <Book: Ten like perhaps ever.>, <Book: Create address impact statement accept.>, <Book: Accept sound treatment easy safe history begin.>, <Book: Gas smile bank like we.>, <Book: Once push perhaps develop eye head thousand.>, <Book: Help beyond court wear serve figure after hope friend.>, <Book: New drive them role fire better nor play.>, <Book: Beyond question price point skill indicate.>, <Book: Want year present result wait president.>, <Book: Body.>, <Book: Stuff meet policy.>, <Book: Thing decision join land important travel behavior fall them.>, <Book: Treatment one share.>, <Book: Degree common information support.>, <Book: Wall movie thus hour animal language lay race.>, <Book: School should guess.>]
>>> 
```

### 2. Export classics

- **Write all books published before 1950 to classic_books.csv with columns title,author,year.**
```
>>> import csv
>>> from library.models import Book
>>> from datetime import date
>>> with open('classic_books.csv', 'w', newline='') as f:
...     writer = csv.writer(f)
...     writer.writerow(['title', 'author', 'year'])
...     writer.writerows([(book.title, book.author.full_name, book.published_on.year) for book in Book.objects.filter(published_on__year__lt=1950).select_related('author')])
... 
19
```
**A new csv `classic_books.csv` is created with column `title`,`author`, and `year`**

### 3. Round‑trip test

- **Delete all books titled “Temporary *” if present.**


- **Import data/temp_books.csv, then immediately dump them back to export_temp_books.csv and verify counts match (rows in = rows out).**

```
>>> from library.models import Book
>>> Book.objects.filter(title__startswith='Temporary').delete()
(0, {})
>>> import csv
>>> from datetime import datetime
>>> books = []
>>> with open('data/temp_books.csv', 'r') as f:
...     reader = csv.DictReader(f)
...     for row in reader:
...         author, _ = Author.objects.get_or_create(full_name=row['author_name'], defaults={'birth_year': int(row['birth_year'])})
...         books.append(Book(title=row['title'], published_on=datetime.strptime(row['published_on'], '%Y-%m-%d').date(), author=author))
... 
>>> Book.objects.bulk_create(books)
[<Book: Temporary Foreign exactly.>, <Book: Temporary It career significant.>, <Book: Temporary We free.>, <Book: Temporary Bag discover end.>, <Book: Temporary Bank hold.>, <Book: Temporary If loss what.>, <Book: Temporary Everybody walk my.>, <Book: Temporary Federal onto board.>, <Book: Temporary Mean physical.>, <Book: Temporary In apply truth.>]
>>> count_in = len(books)
>>> count_in
10
>>> with open('export_temp_books.csv', 'w', newline='') as f:
...     writer = csv.writer(f)
...     writer.writerow(['title', 'author_name', 'published_on', 'birth_year'])
...     writer.writerows([(b.title, b.author.full_name, b.published_on.strftime('%Y-%m-%d'), b.author.birth_year) for b in Book.objects.filter(title__startswith='Temporary').select_related('author')])
... 
43
```
**A new csv `export_temp_books.csv` is created with columns `title`,`author_name`,`published_on`, and `birth_year`**

### 4. Large‑file optimisation

- **Time how long it takes to import a 50 000‑row CSV (generate dummy file if needed). Use bulk_create + iterator to keep memory steady below 100 MB.**

```
>>> import csv
>>> import time
>>> from library.models import Author, Book
>>> from datetime import datetime
>>> start = time.time()
>>> books = []
>>> with open('data/large_books.csv', 'r') as f:
...     reader = csv.DictReader(f)
...     for row in reader:
...         author, _ = Author.objects.get_or_create(full_name=row['author_name'], defaults={'birth_year': int(row['birth_year'])})
...         books.append(Book(title=row['title'], published_on=datetime.strptime(row['published_on'], '%Y-%m-%d').date(), author=author))
...         if len(books) >= 500:
...             Book.objects.bulk_create(books)
...             books = []
... 
[<Book: In around wonder hope reach theory down.>, <Book: Rich trouble cold thing area among.>, <Book: Develop civil month loss author nature.>, <Book: Father mouth citizen.>, <Book: ................
rather property.>, <Book: Quite new receive loss financial it.>, <Book: Another over lot.>, <Book: Material give move past position travel.>, <Book: Fill success see high city land record.>, <Book: Away somebody.>]
>>> print(f"Imported in {time.time() - start} seconds")
Imported in 651.5787076950073 seconds
>>> 
```