from django.db import models

from django.contrib.auth.models import User

from PIL import Image
import os

class Pedido(models.Model):
    class Meta:
          verbose_name = 'Pedido'
          verbose_name_plural = 'Pedidos'

    # pedido é filho de usuário - então se deletar o usuário eu quero que o pedido também seja deletado
    user: models.ForeignKey = models.ForeignKey(User, on_delete=models.CASCADE)
    total: models.FloatField = models.FloatField(default=0)
    qtde_total: models.PositiveBigIntegerField = models.PositiveBigIntegerField(default=0)
    status: models.CharField = models.CharField(
        default='C',
        max_length=1,
        choices=(
            ('A', 'Aprovado'),
            ('C', 'Criado'),
            ('R', 'Reprovado'),
            ('P', 'Pendente'),
            ('E', 'Enviado'),
            ('F', 'Finalizado'),
        )
    )

    def __str__(self):
          return f'{self.user}'

class ItemPedido(models.Model):
    class Meta:
         verbose_name = 'Item do pedido'
         verbose_name_plural = 'Item do pedido'

    pedido: models.ForeignKey = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    produto: models.CharField = models.CharField(max_length=255)
    produto_id: models.PositiveIntegerField = models.PositiveIntegerField()
    variacao: models.CharField = models.CharField(max_length=255)
    variacao_id: models.PositiveIntegerField = models.PositiveIntegerField()
    preco: models.FloatField = models.FloatField()
    preco_promocional: models.FloatField = models.FloatField(default=0)
    quantidade: models.IntegerField = models.IntegerField()
    imagem: models.CharField = models.CharField(max_length=2000)

    def __str__(self):
         return self.produto
