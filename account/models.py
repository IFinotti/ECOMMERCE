from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError

import re
from utils.validacpf import valida_cpf


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                verbose_name='Usuário')
    age = models.PositiveIntegerField(verbose_name="Idade")
    birth_date = models.DateField(verbose_name="Data de nascimento")
    cpf = models.CharField(max_length=11, verbose_name="CPF")
    address = models.CharField(max_length=50, verbose_name="Endereço")
    number = models.CharField(max_length=5, verbose_name="Número")
    complement = models.CharField(max_length=30, verbose_name="Complemento")
    neighborhood = models.CharField(max_length=30, verbose_name="Bairro")
    cep = models.CharField(max_length=8, verbose_name="CEP")
    city = models.CharField(max_length=30, verbose_name="Cidade")
    telephone = models.CharField(
        max_length=13, verbose_name="Telefone (celular)")
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
        ), verbose_name="Estado"
    )

    def __str__(self):
        return f'{self.user}'

    def clean(self):
        error_messages = {}

        cpf_sent = self.cpf or None
        cpf_saved = None
        account = Account.objects.filter(cpf=cpf_sent).first()

        if account:
            cpf_saved = account.cpf

            if cpf_saved is not None and self.pk != account.pk:
                error_messages['cpf'] = 'CPF existente.'

        if not valida_cpf(self.cpf):
            error_messages['cpf'] = 'Digite um CPF válido'

        if re.search(r'[^0-9]', self.cep) or len(self.cep) < 8:
            error_messages['cep'] = 'CEP inválido, digite os 8 digitos do CEP.'

        if error_messages:
            raise ValidationError(error_messages)

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'
