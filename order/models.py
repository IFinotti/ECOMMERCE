from django.db import models
from django.contrib.auth.models import User


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.FloatField()
    total_qtt = models.PositiveIntegerField()
    status = models.CharField(
        default="C",
        max_length=1,
        choices=(
            ('A', 'Approved'),
            ('C', 'Created'),
            ('D', 'Disapproved'),
            ('P', 'Pending'),
            ('S', 'Sent'),
            ('F', 'Finished'),
        )
    )

    def __str__(self):
        return f'Pedido N. {self.pk}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.CharField(max_length=255)
    product_id = models.PositiveIntegerField()
    variation = models.CharField(max_length=255)
    variation_id = models.PositiveIntegerField()
    price = models.FloatField()
    promotional_price = models.FloatField(default=0)
    quantity = models.PositiveIntegerField()
    image = models.CharField(max_length=2000)

    def __str__(self):
        return f'Item do {self.order}'

    class Meta:
        verbose_name = 'Order item'
        verbose_name_plural = 'Order items'
