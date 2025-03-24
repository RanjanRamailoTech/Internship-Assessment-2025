from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class StockPrice(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    price = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)  # For tracking when data is added
    sequence = models.IntegerField()  # To maintain order of stock prices

    class Meta:
        unique_together = ('company', 'sequence')  # Ensure unique sequence per company

    def __str__(self):
        return f"{self.company.name} - {self.price} at {self.timestamp}"