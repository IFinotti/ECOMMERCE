# Generated by Django 5.0.2 on 2024-09-24 02:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='telephone',
            field=models.CharField(default=1, max_length=13),
            preserve_default=False,
        ),
    ]
