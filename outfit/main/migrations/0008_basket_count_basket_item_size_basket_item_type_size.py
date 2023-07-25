# Generated by Django 4.1.5 on 2023-07-25 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_basket'),
    ]

    operations = [
        migrations.AddField(
            model_name='basket',
            name='count',
            field=models.IntegerField(blank=True, default=1, verbose_name='Количество'),
        ),
        migrations.AddField(
            model_name='basket',
            name='item_size',
            field=models.CharField(blank=True, max_length=10, verbose_name='Размер'),
        ),
        migrations.AddField(
            model_name='basket',
            name='item_type_size',
            field=models.CharField(blank=True, max_length=10, verbose_name='Тип размера (страна)'),
        ),
    ]
