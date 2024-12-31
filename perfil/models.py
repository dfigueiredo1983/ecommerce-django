from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

import re
from utils.valida_cpf import valida_cpf

class Perfil(models.Model):
    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'

    usuario: models.OneToOneField = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='usuário')
    idade: models.PositiveIntegerField = models.PositiveIntegerField()
    data_nascimento: models.DateField = models.DateField(blank=True, null=True)
    cpf: models.CharField = models.CharField(max_length=11, verbose_name='CPF')
    endereco: models.CharField = models.CharField(max_length=150)
    numero: models.CharField = models.CharField(max_length=20)
    complemento: models.CharField = models.CharField(max_length=100)
    bairro: models.CharField = models.CharField(max_length=100)
    cep: models.CharField = models.CharField(max_length=8, verbose_name='CEP')
    cidade: models.CharField = models.CharField(max_length=100)
    estado: models.CharField = models.CharField(
        max_length=2,
        default='DF',
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
        return f'{self.usuario.first_name} {self.usuario.last_name}'
    
    def clean(self):
        error_messages = {}
        # print('Valida CPF', valida_cpf(self.cpf))
        if not valida_cpf(self.cpf):
            error_messages['cpf'] = 'Digite um CPF válido.'

        if re.search(r'[^0-9]', self.cep) or len(self.cep) != 8:
            error_messages['cep'] = 'Digite um CEP válido.'

        if error_messages:
            raise ValidationError(error_messages)