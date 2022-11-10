from rest_framework import serializers
from django.db import transaction
from django.conf import settings
from forex_python.converter import CurrencyCodes, CurrencyRates

from .models import Stock


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