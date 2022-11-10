from rest_framework import serializers
from django.db import transaction
from django.conf import settings
from forex_python.converter import CurrencyCodes, CurrencyRates

from .models import Stock, Order


class StockModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'

    def validate(self, data):
        currency = data.get('currency', settings.DEFAULT_CURRENCY)
        data['price'] = CurrencyRates()\
            .convert(currency, settings.DEFAULT_CURRENCY, data['price'])
        
        return data


class StockCreateSerializer(StockModelSerializer):
    currency = serializers.CharField(max_length=3, default=settings.DEFAULT_CURRENCY)

    default_error_messages = {
        'invalid_currency': 
            'Invalid currency. Please see https://www.iban.com/currency-codes for valid currency codes.'
    }

    def validate_currency(self, value):
        currency = CurrencyCodes().get_symbol(value)

        if currency is None:
            self.fail('invalid_currency')
        
        return value
    
    
    @transaction.atomic()
    def create(self, data):
        stock = Stock.objects.create(
            name=data['name'],
            price=data['price']
        )

        return stock

class OrderItemSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    quantity = serializers.IntegerField()
    stock = serializers.SerializerMethodField()

    default_error_messages = {
        'invalid_stock': 'Stock not found.'
    }

    def get_stock(self, data):
        try:
            stock = Stock.objects.get(id=data['id'])
        except Stock.DoesNotExist:
            self.fail('invalid_stock')
        
        return stock
        

class OrderCreateSerializer(serializers.Serializer):
    stocks = OrderItemSerializer(many=True)
    user = serializers.SerializerMethodField()

    def get_user(self, data):
        return self.context['request'].user
    
    def save(self):
        data = self.to_representation(self.validated_data)
        return Order.objects.place(data)

class PortfolioStocksSerializer(serializers.Serializer):
    stock_id = serializers.IntegerField()
    stock_name = serializers.CharField(max_length=255)
    quantity = serializers.IntegerField()
    current_price = serializers.DecimalField(max_digits=99, decimal_places=2)

class PortfolioReadSerializer(serializers.Serializer):
    total_current_value = serializers.DecimalField(max_digits=99, decimal_places=2)
    bought_value = serializers.DecimalField(max_digits=99, decimal_places=2)
    stocks = PortfolioStocksSerializer(many=True)