# Generated by Django 5.0.2 on 2024-02-13 05:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('shortest_description', models.TextField(max_length=255)),
                ('longest_description', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='product_imagens/%Y/%m/')),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
                ('marketing_price', models.FloatField(verbose_name='Preço')),
                ('promotional_marketing_price', models.FloatField(default=0, verbose_name='Preço Promo.')),
                ('type_of', models.CharField(choices=[('V', 'Variable'), ('S', 'Simple')], default='V', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Variation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('price', models.FloatField()),
                ('promotional_price', models.FloatField(default=0)),
                ('stock', models.PositiveIntegerField(default=1)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
            options={
                'verbose_name': 'Variation',
                'verbose_name_plural': 'Variations',
            },
        ),
    ]
