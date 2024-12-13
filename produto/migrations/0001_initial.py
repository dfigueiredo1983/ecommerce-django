# Generated by Django 5.1.4 on 2024-12-11 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('descricao_curta', models.TextField()),
                ('descricao_longa', models.TextField()),
                ('imagem', models.ImageField(blank=True, null=True, upload_to='produto_imagens/%Y/%m')),
                ('slug', models.SlugField(unique=True)),
                ('preco_marketing', models.FloatField(default=0)),
                ('preco_marketing_promocional', models.FloatField(default=0)),
                ('tipo', models.CharField(choices=[('V', 'Variation'), ('S', 'Simple')], default='V', max_length=1)),
            ],
        ),
    ]