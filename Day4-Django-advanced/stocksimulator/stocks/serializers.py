from rest_framework import serializers
from .models import StockPrice, Company

class StockPriceSerializer(serializers.ModelSerializer):
    company = serializers.CharField(source='company.name')

    class Meta:
        model = StockPrice
        fields = ['company', 'price', 'sequence']