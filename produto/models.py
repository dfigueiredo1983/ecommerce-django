from django.db import models

from PIL import Image
import os
from django.conf import settings
from utils.slug_new import slugify_new
from utils import utils

class Produto(models.Model):

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'

    nome: models.CharField = models.CharField(max_length=255)
    descricao_curta: models.TextField = models.TextField()
    descricao_longa: models.TextField = models.TextField()
    imagem: models.ImageField = models.ImageField(
        upload_to='produto_imagens/%Y/%m',
        blank=True,
        null=True,
    )
    slug: models.SlugField = models.SlugField(unique=True, blank=True, null=True)
    preco_marketing: models.FloatField = models.FloatField(default=0, verbose_name='Preço')
    preco_marketing_promocional: models.FloatField = models.FloatField(default=0, verbose_name='Preço Promo')
    tipo: models.CharField = models.CharField(
        default='V',
        max_length=1,
        choices=(
            ('V', 'Variation'),
            ('S', 'Simple')
        )
    )

    def get_preco_formatado(self):
        print('get_preco_formatado')
        # return f'R$ {self.preco_marketing:.2f}'.replace('.', ',')
        return utils.formata_preco(self.preco_marketing)

    def get_preco_marketing_formatado(self):
        # return f'R$ {self.preco_marketing_promocional:.2f}'.replace('.', ',')
        return utils.formata_preco(self.preco_marketing_promocional)

    @staticmethod
    def resize_image(imagem, new_width=800):
        img_full_path = os.path.join(settings.MEDIA_ROOT, imagem.name)

        imagem_pillow = Image.open(img_full_path)
        original_width, original_height = imagem_pillow.size

        if original_width < new_width:
            imagem_pillow.close()
            return

        new_height = round((new_width * original_height) / original_width)
        new_image = imagem_pillow.resize((new_width, new_height), Image.LANCZOS)

        new_image.save(
            img_full_path,
            optimize=True,
            quality=100,
        )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.nome)

        super().save(*args, **kwargs)
        
        max_image_size = 800

        if self.imagem:
            self.resize_image(self.imagem, max_image_size)

    def __str__(self):
        return self.nome


class Variacao(models.Model):

    class Meta:
        verbose_name = 'Variação'
        verbose_name_plural = 'Variações'

    produto: models.ForeignKey = models.ForeignKey(Produto, on_delete=models.CASCADE)
    nome: models.CharField = models.CharField(max_length=50, blank=True, null=True)
    preco: models.FloatField = models.FloatField(verbose_name='Preço')
    preco_promocional:models.FloatField = models.FloatField(default=0, verbose_name='Preço Promo')
    estoque: models.PositiveIntegerField = models.PositiveIntegerField(default=1)

    def get_preco_formatado(self):
        return utils.formata_preco(self.preco)

    def get_preco_promocional_formatado(self):
        return utils.formata_preco(self.preco_promocional)
    
    def __str__(self):
        return self.nome or self.produto

