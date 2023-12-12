from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
from utils.cpf_calc import cpf_calc
import re
# Create your models here.


class Profile(models.Model):
    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveIntegerField()
    birth_date = models.DateField()
    cpf = models.CharField(max_length=11)
    address = models.CharField(max_length=50)
    number = models.CharField(max_length=5)
    complement = models.CharField(max_length=30)
    hood = models.CharField(max_length=30)
    cep = models.CharField(max_length=8)
    city = models.CharField(max_length=30)
    state = models.CharField(
        max_length=2,
        default='SP',
        choices=(
            ('AC', 'Acre'),
            ('AL', 'Alagoas'),
            ('AP', 'Amapá'),
            ('AM', 'Amazonas'),
            ('BA', 'Bahia'),
            ('CE', 'Ceará'),
            ('DF', 'Distrito Federal'),
            ('ES', 'Espírito Santo'),
            ('GO', 'Goiás'),
            ('MA', 'Maranhão'),
            ('MT', 'Mato Grosso'),
            ('MS', 'Mato Grosso do Sul'),
            ('MG', 'Minas Gerais'),
            ('PA', 'Pará'),
            ('PB', 'Paraíba'),
            ('PR', 'Paraná'),
            ('PE', 'Pernambuco'),
            ('PI', 'Piauí'),
            ('RJ', 'Rio de Janeiro'),
            ('RN', 'Rio Grande do Norte'),
            ('RS', 'Rio Grande do Sul'),
            ('RO', 'Rondônia'),
            ('RR', 'Roraima'),
            ('SC', 'Santa Catarina'),
            ('SP', 'São Paulo'),
            ('SE', 'Sergipe'),
            ('TO', 'Tocantins'),
        )
    )

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    def clean(self):
        error_messages = {}

        cpf_sent = self.cpf or None
        cpf_saved = None
        profile = Profile.objects.filter(cpf=cpf_sent).first()

        if profile:
            cpf_saved = profile.cpf
            # if the pk of cpf_saved belongs to the profile, if it's different, the cpf is from another user
            if cpf_saved is not None and self.pk != profile.pk:
                error_messages['cpf'] = 'CPF already exists.'

        if not cpf_calc(self.cpf):
            error_messages['cpf'] = 'Type a valid CPF'

        if re.search(r'[^0-9]', self.cep) or len(self.cep) < 8:
            error_messages['cep'] = 'Type a valid CEP, without letters or symbols.'

        if error_messages:
            raise ValidationError(error_messages)
