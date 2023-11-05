from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveIntegerField()
    birth_date = models
    cpf = models
    address = models
    number = models
    complement = models
    hood = models
    cep = models
    city = models
    state = models
