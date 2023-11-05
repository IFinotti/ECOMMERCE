from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Order(models.Model):
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
