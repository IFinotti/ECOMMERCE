# Generated by Django 5.0.2 on 2024-08-05 20:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_order_merchant_order_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='merchant_order_id',
        ),
    ]
