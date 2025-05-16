from rest_framework import serializers
from stock.models.stock import Stock

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['id', 'company_name', 'current_price']