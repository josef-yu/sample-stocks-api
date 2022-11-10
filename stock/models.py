from django.db import models
from model_utils import models as django_model_utils
from django.contrib.auth.models import User
# Create your models here.

class Stock(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=99, decimal_places=2)

class Order(django_model_utils.TimeStampedModel):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=99, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)