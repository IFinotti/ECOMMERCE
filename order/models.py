from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.FloatField()
    status = models.CharField(
        choices=(
            ('A', 'Approved'),
            ('C', 'Created'),
            ('R', 'Disapproved'),
            ('', ''),
        ),
    )
