# Generated by Django 5.0.2 on 2024-02-13 17:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='OrdemItem',
            new_name='OrderItem',
        ),
    ]
