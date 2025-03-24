from django.db import models

class Stock(models.Model):
    company_name = models.CharField(max_length=100, unique=True)  # Unique to avoid duplicates
    current_price = models.DecimalField(max_digits=12, decimal_places=4)

    def __str__(self):
        return f"{self.company_name} - {self.current_price}"