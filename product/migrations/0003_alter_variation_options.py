# Generated by Django 4.2.6 on 2023-11-04 00:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_variation'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='variation',
            options={'verbose_name': 'Variation', 'verbose_name_plural': 'Variations'},
        ),
    ]
