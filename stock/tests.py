import json
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.reverse import reverse
from django.contrib.auth.models import User
from django.conf import settings
import random

from .models import Stock, Order

# Create your tests here.

SUPER_USERNAME = 'superadminuser'
SUPER_PASSWORD = '!asdkljbneVVZMj241'
SUPER_EMAIL = 'test@test.com'

USERNAME = 'sampleuser'
PASSWORD = 'samplepass12345'
EMAIL = 'test@test.com'

class CreateStockTest(APITestCase):
    def _login(self):
        url = reverse('login')
        data = {
            'username': SUPER_USERNAME,
            'password': SUPER_PASSWORD
        }
        response = self.client.post(url, data)
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + response.json()['auth_token']
            )


    def setUp(self):
        User.objects\
            .create_superuser(
                username=SUPER_USERNAME,
                email=SUPER_EMAIL,
                password=SUPER_PASSWORD
            )
        self._login()
        self.url = reverse('stock-list')
        self.data = {
            'name': 'AAPL',
            'price': 100000.50
        }


        self.data_w_currency = self.data.copy()
        self.data_w_currency['currency'] = 'USD'
    
    def _base_test(self, payload):
        response = self.client.post(self.url, payload)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(data['id'] is not None)
        self.assertTrue(data['currency'] is not None)
        self.assertTrue(data['name'] is not None)
        self.assertTrue(data['price'] is not None)

        if not payload.get('currency', None) is None:
            self.assertTrue(
                data['price'] != payload['price'] and \
                payload['currency'] != settings.DEFAULT_CURRENCY
            )

    def test_can_create_stock(self):
        self._base_test(self.data)
    
    def test_can_create_stock_from_currency(self):
        self._base_test(self.data_w_currency)

class BaseOrderTest(APITestCase):
    def _login(self):
        url = reverse('login')
        data = {
            'username': USERNAME,
            'password': PASSWORD
        }
        response = self.client.post(url, data)
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + response.json()['auth_token']
            )
    
    def _make_stocks(self):
        data = [
            {
                'name': 'AAPL',
                'price': 100000.50
            },
            {
                'name': 'ABKL',
                'price': 2000.25
            }
        ]
        self.stocks = [
            Stock.objects.create(
                name=stock['name'],
                price=stock['price']
            )
            for stock in data
        ]
    
    def setUp(self):
        self.user = User.objects\
            .create_user(
                username=USERNAME,
                email=EMAIL,
                password=PASSWORD
            )
        self._login()
        
        self._make_stocks()

class CreateOrderTest(BaseOrderTest):
    def _get_formatted_data(self):
        payload = [
            {'id': stock.id, 'quantity': random.randint(1, 10)}
            for stock in self.stocks
        ]
        return {'stocks': payload}


    def setUp(self):
        super().setUp()
        self.url = reverse('place-order')
    
    
    def test_can_place_order(self):
        response = self.client.post(self.url, self._get_formatted_data(), format='json')
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(data['order_id'] is not None)
        self.assertTrue(data['total_price'] is not None)


class ReadPortfolioTest(BaseOrderTest):
    def _create_order(self):
        data = {'stocks': [
                {'stock': stock, 'quantity': random.randint(5, 50)}
                for stock in self.stocks
            ],
            'user': self.user
        }
        Order.objects.place(data)
    
    def setUp(self):
        super().setUp()
        for n in range(random.randint(1, 5)):
            self._create_order()
        
        self.url = reverse('view-portfolio')
    
    def test_can_view_portfolio(self):
        response = self.client.get(self.url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(float(data['total_current_value']) >= 0)
        self.assertTrue(float(data['bought_value']) >= 0)
        self.assertTrue(len(data['stocks']) >= 0)


