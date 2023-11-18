from django.db import models
from django.contrib.auth.models import User

import order

# Create your models here.


class Order(models.Model):
    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.FloatField()
    status = models.CharField(
        default="C",
        max_length=1,
        choices=(
            ('A', 'Approved'),
            ('C', 'Created'),
            ('R', 'Disapproved'),
            ('P', 'Pending'),
            ('S', 'Sent'),
            ('F', 'Finished'),
        ),
    )

    def __str__(self):
        return f'Order nº {self.pk}'


class OrderItem(models.Model):
    class Meta:
        verbose_name = 'Order item'
        verbose_name_plural = 'Order items'

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.CharField(max_length=255)
    id_product = models.PositiveIntegerField()
    variation = models.CharField(max_length=255)
    id_variation = models.PositiveIntegerField()
    price = models.FloatField()
    promotional_price = models.FloatField(default=0)
    quantity = models.PositiveIntegerField()
    image = models.CharField(max_length=2000)

    def __str__(self):
        return f'Item of {self.order}'
