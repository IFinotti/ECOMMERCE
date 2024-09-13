from django.db import models
from django.conf import settings

from django.contrib.auth.models import User
from product.models import Variation, Product


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.FloatField()
    qr_code_image = models.ImageField(
        upload_to='pix_qrcodes/', blank=True, null=True)  # Campo para o QR Code
    total_qtt = models.PositiveIntegerField()
    status = models.CharField(
        default="C",
        max_length=1,
        choices=(
            ('A', 'Approved'),  # Aprovado
            ('C', 'Created'),  # Criado
            ('D', 'Disapproved'),  # Desaprovado
            ('P', 'Pending'),  # Pendente
            ('S', 'Sent'),  # Enviado
            ('F', 'Finished'),  # Finalizado
        )
    )

    def __str__(self):
        return f'Pedido N. {self.pk}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE)  # Altere para ForeignKey
    variation = models.CharField(max_length=255)
    variation_id = models.PositiveIntegerField()
    price = models.FloatField()
    promotional_price = models.FloatField(default=0)
    quantity = models.PositiveIntegerField()
    image = models.CharField(max_length=2000)

    @property
    def unit_price(self):
        # Usa o preço promocional se disponível, caso contrário, usa o preço normal
        return self.promotional_price if self.promotional_price > 0 else self.price

    def __str__(self):
        return f'Item do {self.order}'

    class Meta:
        verbose_name = 'Order item'
        verbose_name_plural = 'Order items'
