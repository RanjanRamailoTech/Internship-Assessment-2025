from django.db import models

class Author(models.Model):
    full_name = models.CharField(max_length=255)
    birth_year = models.IntegerField()

    class Meta:
        indexes = [
            models.Index(fields=['birth_year']),
        ]

    def __str__(self):
        return self.full_name

    @classmethod
    def oldest_author(cls):
        return cls.objects.order_by('birth_year').first()

    @classmethod
    def authors_with_books_published_after(cls, year):
        return cls.objects.filter(books__published_on__year__gt=year).distinct().values_list('full_name', flat=True)

class Profile(models.Model):
    author = models.OneToOneField(Author, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return f"Profile of {self.author.full_name}"

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=255)
    published_on = models.DateField()
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)
    is_modern = models.BooleanField(default=False)
    categories = models.ManyToManyField(Category, related_name='books', blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['published_on']),
            models.Index(fields=['title']),
        ]

    def __str__(self):
        return self.title

    @classmethod
    def random_recommendation(cls):
        return cls.objects.order_by('?').first()

    @classmethod
    def bulk_mark_as_modern(cls, year_cutoff):
        return cls.objects.filter(published_on__year__gt=year_cutoff).update(is_modern=True)