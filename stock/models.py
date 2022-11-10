from django.db import models
from model_utils import models as django_model_utils
from django.contrib.auth.models import User
# Create your models here.

class Stock(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=99, decimal_places=2)

class OrderManager(models.Manager):
    def calculate_total_price(self, items):
        return sum(
            item['stock'].price * item['quantity']
            for item in items
        )

    def place(self, data):
        total_price = self.calculate_total_price(data['stocks'])

        order = self.create(
            total_price=total_price,
            user=data['user']
        )

        OrderItem.objects.bulk_create([
            OrderItem(
                order=order,
                stock=item['stock'],
                quantity=item['quantity'],
                price=item['stock'].price
            )
            for item in data['stocks']
        ])

        return order

class Order(django_model_utils.TimeStampedModel):
    total_price = models.DecimalField(max_digits=99, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    objects = OrderManager()

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=99, decimal_places=2)

